from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
from urlparse import urlparse
import uuid
from User.models import User


# def my_upload_to(instance, filename):
#     # "instance" is an instance of Image
#     # return a path here
#     return 'images/' + str(instance.id)
# Create your models here.


class Tag(models.Model):
	tag = models.CharField(max_length= 1000, blank=True)

	def __str__(self):
		return self.tag

#my_upload_to method to change the image title
def my_upload_to(instance, filename):
	# "instance" is an instance of Image
	#split the image extension
	name, extension = os.path.splitext(filename)

	# return a path here, with adding the image extension
	return 'images/' + str(uuid.uuid4()) + extension

class Image(models.Model):
	#Generating unique_id for each image field, to call it in the image URL
	# unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
	# Imagefield to track image path
	image = models.ImageField(upload_to = my_upload_to)

	# Tags will track the many to many relationship with images
	# related_name is the name of the relationship in the images model (ie it is the inverse relationship)
	Tags = models.ManyToManyField(Tag, related_name = 'Images')
	
	# uploaded_by = models.ForeignKey(User, null = True, related_name='uploaded_by')
	# user = models.ManyToManyField(User)
	# user = models.ManyToManyField(UserData, on_delete=models.v, blank=False)
		# def __str__(self):
		# 	return self.user.username
	def __unicode__(self):
	    return os.path.basename(self.image.name)
	# filename = models.CharField(max_length=1000)



