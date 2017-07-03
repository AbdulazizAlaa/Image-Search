from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import (ImageRetrieveSerializer, ImageUploadSerializer,
                                TagSerializer, TagTextSerializer, TagUsernameSerializer)
from rest_framework.views import APIView
from rest_framework import generics
from image.models import Image, Tag, TagText, TagUsername
from app import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
# from engine.nlp.ner import NER
# from engine.nlp.aner import ANER
# from engine.cv.face import opencv_engine
# import numpy as np, cv2, os
from rest_framework import permissions
from langdetect import detect

from engine.cv.vision import vision_engine

import numpy as np
import cv2


# from engine.cv.face import MTCNN_engine
# Create your views here.


class ImageUpload(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        print(request.data)
        image = request.data.get('image')
        uploaded_by = request.user.username
        data = image.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                          'face_recognition': 'facenet',
                                          'object_detection_recognition': 'inception'})

        results = engine.processImage(image)
        print (results)
        objects = results['objects']
        caption =results['captions']
        print (objects)
        for i in objects:
            serializer = TagSerializer(data={'tag': i})
            # print ("hi")
            if(serializer.is_valid()):
                # print ("hadeer")
                serializer.save()
            else:
                print (serializer.errors)
        myjson = {'image': image, 'uploaded_by': uploaded_by, 'caption': caption}
        serializer = ImageUploadSerializer(data=myjson)
        if serializer.is_valid():
            serializer.save()
            print (serializer.data)
            # imgName = serializer.data['image'].split('/')[2]
            # image = Image.objects.filter(image__icontains=imgName)[0]

            # tag = Tag.objects.get(tag="aziz")
            # image.Tags.add(tag)

            # tag = Tag.objects.get(tag="yomna")
            # image.Tags.add(tag)

            # tag = Tag.objects.get(tag="omar")
            # # image.Tags.add(tag)

            # tag = Tag.objects.get(tag="ali")
            # image.Tags.add(tag)

            text = {'status': 1, 'image': serializer.data}
            return Response(text)
        else:
            text = {'status': -1, 'image': serializer.errors}
            return Response(text)


class RenderImage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        text = request.GET.get("q")
        if(type(text) == unicode):
            text = text.encode("ascii", "ignore")

        language = ""
        try:
            language = detect(text)
        except UnicodeDecodeError:
            language = "ar"

        # Params of the serializer
        params = []
        if(language != "ar"):
            # Tags = NER.solve(text)
            Tags = ["Omar", "Hadeer", "Nada"]

            for tag in Tags:
                params.append({'tag': tag})
        else:
            # call Arabic model...
            # arabic_model = ANER.ANER()
            # Tags = arabic_model.solve(text)
            Tags = ["arabic_name", "arabic_name", "arabic_name"]

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
                tag_models = Tag.objects.filter(tag=tag)

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
                        img = cv2.imread(image.image.url, 1)  # change this with any other image on your computer
                        [img, faces, faces_rects] = f.crop_faces(img)

                        cv2.imwrite('media/images/tmp/' + filename, img)
                        output.append('/media/images/tmp/' + filename)

                    # # For each image in the tag model
                    # for image in tag_model.Images.all():
                    #   output.append("/" + str(image.image.url))

            text = {'status': 1, 'images': output}
        else:
            text = {'status': -1, 'images': serializer.errors}
        return JsonResponse(text)


# Get Image and apply face detection algorithm on it
# then send the image back w/ coordinates, width, height
class FaceDetection(APIView):
  def post(self, request):
      image_data = request.data.get('image')

      data = image_data.read()
      # convert the image to a NumPy array and then read it into
      # OpenCV format
      image = np.asarray(bytearray(data), dtype="uint8")
      image = cv2.imdecode(image, cv2.IMREAD_COLOR)

      engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                          'face_recognition': 'facenet',
                                          'object_detection_recognition': 'inception'})
      results = engine.processImage(image)
      return Response(results)


class AddTag(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # print(request.data)
        # Get username by adding the token in header:
        # Authorization: JWT token
        user = request.user.username
        print (user)
        # text_tag = []
        text_tag = request.data.get("tag_text")
        # print text_tag
        # username_tag = []
        username_tag = request.data.get("tag_username")
        # print text_tag
        image = request.data.get("image")

        jsonText_TagText = {'image': image, 'tag': text_tag, 'user': user}
        # print jsonText_TagText
        jsonText_TagUsername = {'image': image, "tag": username_tag, 'user': user}
        # print jsonText_TagText
        # print jsonText_TagUsername
        tagArray = text_tag
        # for tag in text_tag:
        #     tagArray.append(tag)
        # # print tagArray
        serializer_tag = TagSerializer(data=tagArray)
        serializer_text_tag = TagTextSerializer(data=jsonText_TagText)
        serializer_username_tag = TagUsernameSerializer(data=jsonText_TagUsername)
        # print serializer_username_tag.is_valid()
        # print serializer_username_tag.errors
        # print MTCNN_engine.
        if(serializer_tag.is_valid()):
            # print serializer_tag.validated_data
            # print serializer_tag.data
            serializer_tag.save()
            # print "tags saved in table Tags"
        # print jsonText_TagText
        if(serializer_text_tag.is_valid()):
            # print serializer_text_tag.validated_data
            serializer_text_tag.save()
        # print serializer_text_tag.data
        # print serializer_text_tag.errors
        # print serializer_username_tag.is_valid()
        if(serializer_username_tag.is_valid()):
            # print serializer_username_tag.data
            serializer_username_tag.save()
        # print serializer_username_tag.errors

        # # print serializer_text_tag.data
        # print serializer_text_tag.is_valid()
        # print serializer_text_tag.validated_data
        # print serializer_text_tag.errors
        print (serializer_username_tag.is_valid())
        print (serializer_username_tag.data)
        print (serializer_username_tag.errors)
        return Response()


class getUsername(APIView):
    def get(self, request):
        q = request.GET.get("q")
        # icontains acts as LIKE in sql, icontains is case insensitive
        search = User.objects.filter(username__icontains=q).values_list('username')
        print (search)
        text = {'results': list(search)}
        print (text)
        return Response(text)
