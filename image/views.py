from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag

# Create your views here.
class ImageUpload(generics.CreateAPIView):

	queryset = Image.objects.all()
	serializer_class = ImageSerializer

class RenderImage(generics.CreateAPIView):

	queryset = Tag.objects.all()
	serializer_class = TagSerializer
