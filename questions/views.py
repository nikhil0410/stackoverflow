from django.shortcuts import render,render_to_response,redirect
from django.views.generic import CreateView,FormView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout


from django.template import RequestContext

from .models import Question
from .forms import SignUpForm,LoginForm
from stackoverflow.mixin import NextUrlMixin,RequestFormAttachMixin

# Create your views here.
def question_list(request):
	question = Question.objects.all()
	context = {
		'questions': question
	}
	return render(request,'questions/list.html',context)

# class RegisterView(CreateView):
# 	form_class = RegistrationForm
# 	template_name = 'questions/register.html'
# 	success_url = '/login/'

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('signup')
	else:
		form = SignUpForm()
	return render(request, 'questions/register.html', {'form': form})

class LoginView(NextUrlMixin,RequestFormAttachMixin, FormView):
	form_class = LoginForm
	success_url='/'
	template_name = 'questions/login.html'
	default_next = '/'

	def form_valid(self,form):
		next_path = self.get_next_url()
		return redirect(next_path)

def login_user(request):
	logout(request)
	username = password = ''
	form_class = LoginForm
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/main/')
	return render(request,'questions/login.html',{'form':form_class})


class CreateQuestion(CreateView):
	model = Question
	fields = ['title','description']
	template_name = 'questions/create-question.html'


class QuestionDetailView(DetailView):
	template_name = 'questions/detail_view.html'
	model = Question

	def get_object(self,*args,**kwargs):
		request = self.request 
		slug = self.kwargs.get('slug')

		try:
			instance = Question.objects.filter(slug=slug).first()
		except Question.DoesNotExist:
			raise Http404('Question does not exist')
		except Question.MultipleObjectReturned:
			qs = Question.objects.filter(slug=slug)
			instance = qs.first()
		except :
			raise http404('Dont know what you have done there')

		# print(instance.values())
		return instance





























