from User.models import UserData
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserDataSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message="This email already exists.")])

	class Meta:
		model = User
		#fields I want only
		fields = ('username', 'first_name','last_name', 'password', 'email')
