from image.models import Image, Tag, TagText, TagUsername
from User.serializers import UserTagSerializer, UserLoginSerializer
# from django.contrib.auth.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):

	tag = serializers.CharField()

	class Meta:
		model = Tag
		# Input to the tag serializer
		fields = ['tag']

class ImageRetrieveSerializer(serializers.ModelSerializer):#test
	# image = serializers.CharField()
	#id = serializers.IntegerField()
	# Parameter many was used to serialize a list instead of 1 string
	Tags = TagSerializer(required=True, many=True)
	# image_url = serializers.SerializerMethodField('get_image_url')
	# image = serializers.ImageField(max_length=None, use_url=True)

	class Meta:
		model = Image
		# The input to the ImageRetrieveSerializer
		# This should include the input to the TagSerializer
		fields = ('__all__')


class ImageUploadSerializer(serializers.ModelSerializer):#test

	# tag = TagSerializer(many = True, read_only=True)#ques
	# image_url = serializers.SerializerMethodField('get_image_url')
	image = serializers.ImageField(max_length=None, use_url=True)
	uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Image
		fields = ('__all__')


	# def get_image_url(self, obj):
	# 	return obj.image.url

class TagTextSerializer(serializers.ModelSerializer):
	tag = TagSerializer( required=True, many = True)
	user = serializers.SlugRelatedField(queryset = User.objects.all(),  slug_field = "username")
	# image = serializers.SlugRelatedField(queryset = Image.objects.all(), slug_field = "image")

	class Meta:
		model = TagText
		fields = ('tag', 'user',)

class TagUsernameSerializer(serializers.ModelSerializer):
	tag = UserTagSerializer(required=True, many = True)
	user = serializers.SlugRelatedField(queryset = User.objects.all(),  slug_field = "username")
	# image = serializers.SlugRelatedField(queryset = Image.objects.all(), slug_field = "image")
	class Meta:
		model = TagUsername
		fields = ('tag', 'user',)
