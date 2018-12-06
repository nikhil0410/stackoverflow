from django.db import models

class Tag(models.Model):
	title       = models.CharField(max_length=120)
	timestamp   = models.DateTimeField(auto_now_add=True)
	active      = models.BooleanField(default=True)

	def __str__(self):
		return self.title