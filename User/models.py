from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class UserData(models.Model):
		# name = models.CharField(max_length=100,null = True)
		user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)



class Image(models.Model):
	image = models.ImageField(upload_to = "images/" )

		# def __str__(self):
		# 	return self.user.username


# Create your models here