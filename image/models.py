from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
from urlparse import urlparse
from uuid import uuid4

# Create your models here.
class Image(models.Model):
	# def path_and_rename(path):
	#     def wrapper(instance, filename):
	#         ext = filename.split('.')[-1]
	#         # get filename
	#         if instance.pk:
	#             filename = '{}.{}'.format(instance.pk, ext)
	#         else:
	#             # set filename as random string
	#             filename = '{}.{}'.format(uuid4().hex, ext)
	#         # return the whole path to the file
	#         return os.path.join(path, filename)
	#     return wrapper
	image = models.ImageField(upload_to = "images/")
	# uploaded_by = models.ForeignKey(User, null = True)
	# user = models.ManyToManyField(User)
	# user = models.ManyToManyField(UserData, on_delete=models.v, blank=False)
		# def __str__(self):
		# 	return self.user.username
	def __unicode__(self):
	    return os.path.basename(self.image.name)
	# filename = models.CharField(max_length=1000)


# Create your models here
