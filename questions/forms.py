from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class RegistrationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

	class Meta:
		model = User 
		fields = ('first_name','email')

	def cleanPassword(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2 and password1 and password2:
			raise forms.ValidationError('Please enter the same password')
		return password2

	def save(self,commit=True):

		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	email    = forms.EmailField(label='Email')
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(LoginForm, self).__init__(*args, **kwargs)
	def authenticates(self, username=None, password=None, **kwargs):
		UserModel = get_user_model()
		try:
			user = User.objects.get(email=username)
		except User.DoesNotExist:
			return None
		else:
			if user.check_password(password):
				return user
		return None

	def clean(self):
		request = self.request
		data = self.cleaned_data
		email  = data.get("email")
		password  = data.get("password")
		qs = User.objects.filter(email=email)
		print(qs)
		if qs.exists():
			# user email is registered, check active/
			not_active = qs.filter(is_active=False)
			if not_active.exists():
				## not active, check email activation
				link = reverse("account:resend-activation")
				reconfirm_msg = """Go to <a href='{resend_link}'>
				resend confirmation email</a>.
				""".format(resend_link = link)
				confirm_email = EmailActivation.objects.filter(email=email)
				is_confirmable = confirm_email.confirmable().exists()
				if is_confirmable:
					msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
					raise forms.ValidationError(mark_safe(msg1))
				email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
				if email_confirm_exists:
					msg2 = "Email not confirmed. " + reconfirm_msg
					raise forms.ValidationError(mark_safe(msg2))
				if not is_confirmable and not email_confirm_exists:
					raise forms.ValidationError("This user is inactive.")
		user = self.authenticates( username=email, password=password)
		print(email,password,user)
		if user is None:
			raise forms.ValidationError("Invalid credentials")
		login(request, user)
		self.user = user
		return data