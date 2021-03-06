from django.db import models
from questions.models import Question
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Answers(models.Model):
	question_id 		= models.ForeignKey(Question,on_delete=None)
	user 				= models.ForeignKey(User,on_delete=None)
	answer_description 	= models.TextField()
	upvote_count		= models.IntegerField(default=0)
	downvote_count		= models.IntegerField(default=0)
	total_count			= models.IntegerField(default=0)
	featured        	= models.BooleanField(default=False)
	active          	= models.BooleanField(default=True)
	timestamp      	 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.answer_description or ''

class AnswersComment(models.Model):
	answer_id 				= models.ForeignKey(Answers,on_delete=None)
	user 					= models.ForeignKey(User,on_delete=None)
	comment_description 	= models.TextField()
	upvote_count			= models.IntegerField(default=0)
	downvote_count			= models.IntegerField(default=0)
	total_count				= models.IntegerField(default=0)
	featured        		= models.BooleanField(default=False)
	active          		= models.BooleanField(default=True)
	timestamp      	 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.comment_description or ''
