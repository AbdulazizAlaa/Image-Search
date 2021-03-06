from image.models import Image
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserDataSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message="This email already exists.")])

	class Meta:
		model = User
		#fields I want only
		fields = ('username', 'first_name','last_name', 'password', 'email')


class UserLoginSerializer(serializers.ModelSerializer):


	class Meta:
		model = User
		#fields I want only
		fields = ('username',  'password',)

class UserTagSerializer(serializers.ModelSerializer):
	# username = serializers.CharField()

	class Meta:
		model = User
		#fields I want only
		fields = ('id', )


class UsernameTagSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = User
        # fields I want only
        fields = ('username', )
        # To avoid the unique validator constraint
        extra_kwargs = {
            'username': {'validators': []},
        }

class ImageSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None, use_url=True)
	class Meta:
		model = Image
