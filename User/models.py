from __future__ import unicode_literals
from django.db import models

class UserData(models.Model):
		username = models.CharField(max_length=20, unique=True)
		name = models.CharField(max_length=100,null = True)
		email = models.EmailField(max_length=100, unique = True)
		password = models.CharField(max_length=30)
		def __str__(self):
			return self.name


# Create your models here