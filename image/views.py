from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag

# Create your views here.
class ImageUpload(APIView):

	# queryset = Image.objects.all()
	# serializer_class = ImageSerializer
	def post(self, request, format=None):
		print("in 1")
		serializer = ImageSerializer(data=request.data)
		print("in 2")
		print(request.data)
		print (serializer.is_valid())
		if serializer.is_valid():
			print("in 3")
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)
		print(serializer.errors)
class RenderImage(generics.CreateAPIView):

	queryset = Tag.objects.all()
	serializer_class = TagSerializer
