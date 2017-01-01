from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag
from django.http import JsonResponse
# Create your views here.
class ImageUpload(APIView):

	# queryset = Image.objects.all()
	# serializer_class = ImageSerializer
	def post(self, request, format=None):
		print("in 1")
		print(request.data)
		serializer = ImageSerializer(data=request.data)
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
	def post(self, request):
		print(request.data)
		serializer = ImageSerializer(data = request.data)
		print(serializer.is_valid())
		if(serializer.is_valid()):
			print("1")
			tags = serializer.data['tag']
			output = {}
			images = Image.objects.get(id = tags)
			print("2")
			# output['image'] = serializer.data
			for image in images:
				output.append(image.url)
			text = {'status': 1, 'data':output}
		else:
			text = {'status':-1, 'data':serializer.errors}
		return JsonResponse(text)
		# serializer = TagSerializer(data = request.data)
		# if(serializer.is_valid()):
		# 	serializer.save()