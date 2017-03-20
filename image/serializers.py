from image.models import Image, Tag
from user.serializers import UserDataSerializer
# from django.contrib.auth.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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
		fields = ['Tags']


class ImageUploadSerializer(serializers.ModelSerializer):#test
	
	# tag = TagSerializer(many = True, read_only=True)#ques
	# image_url = serializers.SerializerMethodField('get_image_url')
	# image = serializers.ImageField(max_length=None, use_url=True)
	
	class Meta:
		model = Image
		fields = ('image',)


	# def get_image_url(self, obj):
	# 	return obj.image.url

class TagTextSerializer(serializers.ModelSerializer):

	tag = TagSerializer(required=True, many=True)
	image = ImageUploadSerializer(required=True, many=True)
	user = UserDataSerializer(many=True)

	class Meta:
		model = TagText
		fields = ('tag', 'image', 'user')

class TagUsernameSerializer(serializers.ModelSerializer):

	tag = UserDataSerializer(required=True, many=True)
	image = ImageUploadSerializer(required=True, many=True)
	user = UserDataSerializer(many=True)

	class Meta:
		model = TagUsername
		fields = ('tag', 'image', 'user')