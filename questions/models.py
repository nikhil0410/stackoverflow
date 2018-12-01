
import random
import os
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from froala_editor.fields import FroalaField
from stackoverflow.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Question(models.Model):
	title           = models.CharField(max_length=120)
	user 			= models.ForeignKey(User, null=True, blank=True, on_delete=None)
	slug            = models.SlugField(blank=True, unique=True)
	description     = FroalaField()
	upvote_count	= models.IntegerField(default=0)
	downvote_count	= models.IntegerField(default=0)
	total_count		= models.IntegerField(default=0)
	featured        = models.BooleanField(default=False)
	active          = models.BooleanField(default=True)
	timestamp       = models.DateTimeField(auto_now_add=True)
	views			= models.IntegerField(default=0)



	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse("question:question-answers", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title


def question_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(question_pre_save_receiver, sender=Question) 

class QuestionComment(models.Model):
	question_id 			= models.ForeignKey(Question,on_delete=None)
	user 					= models.ForeignKey(User,on_delete=None)
	comment_description 	= FroalaField()
	upvote_count			= models.IntegerField(default=0)
	downvote_count			= models.IntegerField(default=0)
	total_count				= models.IntegerField(default=0)
	featured        		= models.BooleanField(default=False)
	active          		= models.BooleanField(default=True)
	timestamp      	 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.comment_description 


def question_total_count(sender, instance, *args, **kwargs):
	instance.total_count = instance.upvote_count - instance.downvote_count
	print(instance.total_count)
	# instance.save()

pre_save.connect(question_total_count, sender = Question)
pre_save.connect(question_total_count, sender = QuestionComment)