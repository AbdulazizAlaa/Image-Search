from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class UserData(models.Model):
<<<<<<< HEAD
		# name = models.CharField(max_length=100,null = True)
		user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)



class Image(models.Model):
	image = models.ImageField(upload_to = "images/" )
	# def __str__ (self):
	# 	return self.image.url
=======
		#name = models.CharField(max_length=100,null = True)
		user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

		def __str__(self):
			return self.user.username


# Create your models here
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
