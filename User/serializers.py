<<<<<<< HEAD
from User.models import UserData, Image
=======
from User.models import UserData
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserDataSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message="This email already exists.")])

	class Meta:
		model = User
		#fields I want only
		fields = ('username', 'first_name','last_name', 'password', 'email')
<<<<<<< HEAD

class ImageSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None, use_url=True)
	class Meta:
		model = Image
=======
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
