from image.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class ImageSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None, use_url=True)
	class Meta:
		model = Image