from __future__ import unicode_literals
from django.db import models
from rest_framework import serializers
from rest_framework import validators


class User(models.Model):
		username = models.CharField(max_length=20, unique=True)
		name = models.CharField(max_length=50)
		email = models.EmailField(max_length=100)
		password = models.CharField(max_length=30)

# Create your models here