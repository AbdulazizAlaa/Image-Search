from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageRetrieveSerializer, ImageUploadSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag
from app import settings
from django.http import JsonResponse
#from engine.nlp.ner import NER
from rest_framework import permissions

# Create your views here.
class ImageUpload(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def post(self, request, format=None):
		print("in 1")
		print(request.data)
		serializer = ImageUploadSerializer(data=request.data)
		print("in 2")
		print(request.data)
		print (serializer.is_valid())
		print(serializer.errors)
		if serializer.is_valid():
			print("in 3")
			serializer.save()
			text = {'status': 1, 'image':serializer.data}
			return Response(text)
		else:
			text = {'status':-1, 'image':serializer.errors}
			return Response(text)
		
class RenderImage(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, format = None):

		text = request.GET.get("q")
		if(type(text) == unicode):
			text = text.encode("ascii", "ignore")

		#Tags = NER.solve(text)
		#Tags = ["Omar", "Hadeer", "Nada"]
		# Params of the serializer
		params = []
		for tag in Tags:
			params.append({'tag': tag})

		# Serialize input data
		serializer = ImageRetrieveSerializer(data={'Tags': params})
		
		# Array for all images urls
		output = []
		
		# Check validation
		if(serializer.is_valid()):
			# Check if no tags
			if len(Tags) == 0:
				return JsonResponse({'status': 1, 'images': []})

			# For each Tag, get all images it is in
			# And append their URLs to the output
			for tag in Tags:
				# Get return image instance
				tag_models = Tag.objects.filter(tag = tag)

				# For each model, get its images' URLs
				for tag_model in tag_models:
					if len(tag_model.Images.all()) == 0:
						continue

					# For each image in the tag model
					for image in tag_model.Images.all():
						output.append("/" + str(image.image.url))
				
			text = {'status': 1, 'images':output}
		else:
			text = {'status':-1, 'images':serializer.errors}
		return JsonResponse(text)
