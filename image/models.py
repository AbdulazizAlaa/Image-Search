from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
from urlparse import urlparse
from uuid import uuid4
from User.models import User, UserData


# def my_upload_to(instance, filename):
#     # "instance" is an instance of Image
#     # return a path here
#     return 'images/' + str(instance.id)
# Create your models here.


class Tag(models.Model):
	tag = models.CharField(max_length= 1000, blank=True)

	def __str__(self):
		return self.tag

class Image(models.Model):
	# Imagefield to track image path
	image = models.ImageField(upload_to = 'images/')

	# Tags will track the many to many relationship with images
	# related_name is the name of the relationship in the
	# images model (ie it is the inverse relationship)
	Tags = models.ManyToManyField(Tag, related_name = 'Images')
	# uploaded_by = models.ForeignKey(User, null = True, related_name='uploaded_by')
	# user = models.ManyToManyField(User)
	# user = models.ManyToManyField(UserData, on_delete=models.v, blank=False)
		# def __str__(self):
		# 	return self.user.username
	def __unicode__(self):
	    return os.path.basename(self.image.name)
	# filename = models.CharField(max_length=1000)



