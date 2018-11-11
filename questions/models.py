
import random
import os
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from stackoverflow.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

# Create your models here.
class Question(models.Model):
	title           = models.CharField(max_length=120)
	user 			= models.ForeignKey(User, null=True, blank=True, on_delete=None)
	slug            = models.SlugField(blank=True, unique=True)
	description     = models.TextField()
	featured        = models.BooleanField(default=False)
	active          = models.BooleanField(default=True)
	timestamp       = models.DateTimeField(auto_now_add=True)



	# def get_absolute_url(self):
	# 	#return "/products/{slug}/".format(slug=self.slug)
	# 	return reverse("products:detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title


def question_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(question_pre_save_receiver, sender=Question) 