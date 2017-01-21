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
from engine.nlp.ner import NER
from django.contrib.sites.models import Site
# Create your views here.
class ImageUpload(APIView):

	# queryset = Image.objects.all()
	# serializer_class = ImageSerializer
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
			# print(request.data['image'])
			# temp = Image.objects.get(id = request.data['image'])
			# print(temp)
			text = {'status': 1, 'data':serializer.data}
			return Response(text)
		else:
			text = {'status':-1, 'data':serializer.errors}
			return Response(text)
		
class RenderImage(APIView):
	def get(self, request, format = None):

		Tags = NER.solve(request.GET.get("q"))
		#Tags = ["Nada", "Omar"]
		
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
				return JsonResponse({'status': 1, 'data': []})

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
				
			text = {'status': 1, 'data':output}
		else:
			text = {'status':-1, 'data':serializer.errors}
		return JsonResponse(text)


		# serializer = TagSerializer(data = request.data)
		# if(serializer.is_valid()):
		# 	serializer.save()