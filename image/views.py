from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import ImageRetrieveSerializer, ImageUploadSerializer, TagSerializer, TagTextSerializer, TagUsernameSerializer
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag, TagText, TagUsername
from app import settings
from django.http import JsonResponse
#from engine.nlp.ner import NER
#from engine.cv.face import opencv_engine
#import numpy as np, cv2, os
from rest_framework import permissions
# from engine.cv.face import MTCNN_engine
# Create your views here.
# class ImageUpload(APIView):
# 	permission_classes = (permissions.IsAuthenticated,)
#
# 	def post(self, request, format=None):
# 		print(request.data)
# 		serializer = ImageUploadSerializer(data=request.data)
#
# 		if serializer.is_valid():
# 			serializer.save()
# 			print serializer.data
# 			imgName = serializer.data['image'].split('/')[2]
# 			image = Image.objects.filter(image__icontains=imgName)[0]
#
# 			tag = Tag.objects.get(tag="aziz")
#         		image.Tags.add(tag)
#
# 		        tag = Tag.objects.get(tag="yomna")
#             		image.Tags.add(tag)
#
#             		tag = Tag.objects.get(tag="omar")
#             		#image.Tags.add(tag)
#
#             		tag = Tag.objects.get(tag="ali")
#             		image.Tags.add(tag)
#
# 			text = {'status': 1, 'image':serializer.data}
# 			return Response(text)
# 		else:
# 			text = {'status':-1, 'image':serializer.errors}
# 			return Response(text)

class RenderImage(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, format = None):

		text = request.GET.get("q")
		if(type(text) == unicode):
			text = text.encode("ascii", "ignore")

		#Tags = NER.solve(text)
		Tags = ["Omar", "Hadeer", "Nada"]
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


					if not os.path.exists('media/images/tmp'):
						os.mkdir('media/images/tmp')
					# opencv_engine decleration
					f = opencv_engine.OpenCVFaceEngine("engine")

					# For each image call the face detection module
					for image in tag_model.Images.all():
						filename = image.image.url.split('/')[2]
						img = cv2.imread(image.image.url, 1) #change this with any other image on your computer
						[img, faces, faces_rects] = f.crop_faces(img)

						cv2.imwrite('media/images/tmp/'+filename, img)
						output.append('/media/images/tmp/'+filename)

					# # For each image in the tag model
					# for image in tag_model.Images.all():
					# 	output.append("/" + str(image.image.url))

			text = {'status': 1, 'images':output}
		else:
			text = {'status':-1, 'images':serializer.errors}
		return JsonResponse(text)


# Get Image and apply face detection algorithm on it
# then send the image back w/ coordinates, width, height
# class FaceDetection(APIView):
# 	def post(self, request):
# 		myimage = request.data



class UploadImage(APIView):
	# permission_classes = (permissions.IsAuthenticated,)
	def post(self, request):
		print (request.data)
		# text_tag = []
		text_tag = request.data.get("tag_text")
		print text_tag
		# username_tag = []
		username_tag = request.data.get("tag_username")
		user = request.data.get("user")
		image = request.data.get("image")
		# print text_tag
		# print username_tag
		# print uploaded_by
		# print image

		jsonText_TagText = {'image':image, 'tag':text_tag, 'user':user}
		jsonText_TagUsername = {'image':image, "tag":username_tag,'user':user}
		print "hiii"
		tagArray = []
		for tag in text_tag:
			tagArray.append(tag)
		print tagArray
		serializer_tag = TagSerializer(data = tagArray, many = True)
		serializer_text_tag = TagTextSerializer(data = jsonText_TagText)
		# serializer_username_tag = TagUsernameSerializer(data = jsonText_TagUsername)
		# print serializer_username_tag.is_valid()
		# print serializer_username_tag.errors
		# print MTCNN_engine.
		if(serializer_tag.is_valid()):
			serializer_tag.save()
			print "tags saved in table Tags"

		if(serializer_text_tag.is_valid()):
			print "text tags are saved in text tags"
		print serializer_text_tag.errors
		# if(serializer_username_tag.is_valid()):
		# 	print "username tags are saved in text tags"
			# print serializser_text_tag.errors
			# print serializer_text_tag.data
