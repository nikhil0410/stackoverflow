from django.shortcuts import render,render_to_response,redirect
from django.views.generic import CreateView,FormView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Question,QuestionComment
from answers.models import Answers,AnswersComment
from .forms import SignUpForm,LoginForm, AnswerForm, AnswerCommentForm, QuestionCommentForm
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

# def login_user(request):
# 	logout(request)
# 	username = password = ''
# 	form_class = LoginForm
# 	if request.POST:
# 		username = request.POST['username']
# 		password = request.POST['password']

# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				login(request, user)
# 				return HttpResponseRedirect('/main/')
# 	return render(request,'questions/login.html',{'form':form_class})


class CreateQuestion(CreateView):
	model = Question
	fields = ['title','description']
	template_name = 'questions/create-question.html'

	def form_valid(self,form):
		# form = form.save(commit=False)
		# print(form.user)
		form.instance.user = self.request.user 
		# a = form.save()
		# print(a)
		return super().form_valid(form)



class QuestionDetailView(FormMixin, DetailView):
	template_name = 'questions/detail_view.html'
	model = Question
	form_class = AnswerForm

	def get_context_data(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
		question = Question.objects.filter(slug=slug).first()
		answer = Answers.objects.filter(question_id = question.id)
		context['answer'] = answer
		context['form'] = self.get_form()
		return context

	def get_object(self,*args,**kwargs):
		request = self.request 
		slug = self.kwargs.get('slug')

		try:
			instance = Question.objects.filter(slug=slug).first()
			answer = Answers.objects.filter(question_id = instance.id)
		except Question.DoesNotExist:
			raise Http404('Question does not exist')
		except :
			raise http404('Dont know what you have done there')

		# print(instance.values())
		return instance

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		# Here, we would record the user's interest using the message
		# passed in form.cleaned_data['message']
		return super().form_valid(form)




def QuestionAnswers(request, slug=None, *args, **kwargs):
	template_name = 'questions/detail_view.html'
	instance = Question.objects.filter(slug=slug).first()
	ans_comments = AnswersComment.objects.filter(answer_id__question_id = instance)
	qus_comments = QuestionComment.objects.filter(question_id = instance)
	print(1)
	if request.method == 'POST':
		print('inside post')
		if request.POST.get('answer'):
			answer_coment_form = AnswerCommentForm(request.POST)
			print(answer_coment_form)
			if answer_coment_form.is_valid():
				ans_cmnt_form = answer_coment_form.save(commit = False)
				ans_cmnt_form.user = request.user
				ans_instance = Answers.objects.filter(pk=request.POST.get('answer_obj'))
				ans_cmnt_form.answer_id = ans_instance.first()
				ans_cmnt_form.save()
		elif request.POST.get('question'):
			question_coment_form = QuestionCommentForm(request.POST)
			if question_coment_form.is_valid():
				qus_cmnt_form = question_coment_form.save(commit = False)
				qus_cmnt_form.user = request.user
				qus_cmnt_form.question_id = instance
				qus_cmnt_form.save()


		else:
			form = AnswerForm(request.POST)
			if form.is_valid():
				ans = form.save(commit = False)
				ans.user = request.user 
				ans.question_id = instance
				ans.save()

	# else:
	form_class = AnswerForm()
	
	if instance is None:
		raise Http404('No question found')

	answer = Answers.objects.filter(question_id = instance.id)
	context = {
		'object': instance,
		'answer': answer,
		'ans_comments': ans_comments,
		'qus_comments': qus_comments 
	}
	print(ans_comments.values())
	context['form'] = form_class
	context['answer_coment_form'] = AnswerCommentForm
	context['question_coment_form'] = QuestionCommentForm
	return render(request,template_name,context)

def user_logout(request):
	logout(request)
	return render(request,'questions/list.html')






















