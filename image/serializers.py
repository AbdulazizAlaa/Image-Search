from image.models import Image, Tag
# from django.contrib.auth.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class ImageSerializer(serializers.ModelSerializer):

	# image_url = serializers.SerializerMethodField('get_image_url')
	# image = serializers.ImageField(max_length=None, use_url=True)
	
	class Meta:
		model = Image
		fields = ('id', 'image')

	# def get_image_url(self, obj):
	# 	return obj.image.url

class TagSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Tag
		# fields = ('field', 'image', 'image_url')
