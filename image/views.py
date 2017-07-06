from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from image.serializers import (ImageRetrieveSerializer, ImageUploadSerializer,
                                TagSerializer, TagTextSerializer, TagUsernameSerializer,
                                TagUsernameRectangleSerializer, TagTextRectangleSerializer)
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


class ImageUpload(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        print(request.data)
        image = request.data.get('image')
        uploaded_by = request.user.username
        myjson = {'image': image, 'uploaded_by': uploaded_by, 'caption': 'caption'}
        serializer = ImageUploadSerializer(data=myjson)
        if serializer.is_valid():
            serializer.save()
            print (serializer.data)


            # image_file = serializer.data['image']

            # image_data = cv2.imread(image_file)

            # engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
            #                                   'face_recognition': 'facenet',
            #                                   'object_detection_recognition': 'inception'})

            # results = engine.processImage(image_data)

            # objects = results['objects']
            # caption = results['captions']
            # print (objects)
            # for i in objects:
            #     tag_serializer = TagSerializer(data={'tag': i})
            #     # print ("hi")
            #     if(tag_serializer.is_valid()):
            #         # print ("hadeer")
            #         tag_serializer.save()
            #     else:
            #         print (tag_serializer.errors)

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
        # Get username by adding the token in header:
        # Authorization: JWT token
        user = request.user.username
        text_tag = request.data.get("tag_text")
        username_tag = request.data.get("tag_username")
        image = request.data.get("image")
        jsonText_TagText = {'image': image,
                            'tag': text_tag,
                            'user': user}

        jsonText_TagUsername = {'image': image,
                                "tag": username_tag,
                                'user': user}
        tagArray = []
        for obj in enumerate(text_tag):
            tagArray.append({'tag': obj[1]['tag']})
        # print (tagArray)

        serializer_tag = TagSerializer(data=tagArray, many=True)
        # print (serializer_tag.is_valid())
        serializer_text_tag = TagTextSerializer(data=jsonText_TagText)
        serializer_username_tag = TagUsernameSerializer(data=jsonText_TagUsername)

        if(serializer_tag.is_valid()):
            try:
                serializer_tag.save()
            except:
                print("duplicate")
                pass
            print ('tags saved')
            if(serializer_text_tag.is_valid()):
                serializer_text_tag.save()
                print ('tags text saved')
            if(serializer_username_tag.is_valid()):
                serializer_username_tag.save()
                print ('tags username saved')

            id_username = serializer_username_tag.data['id']
            id_text = serializer_text_tag.data['id']

            rect = []
            # Save rectangles of the tags of username
            for obj in enumerate(username_tag):
                temp = {'width': obj[1]['width'],
                        'length': obj[1]['length'],
                        'xCoordinate': obj[1]['xCoordinate'],
                        'yCoordinate': obj[1]['yCoordinate'],
                        'tag_username': id_username}
                rect.append(temp)
            # print (rect)
            ser = TagUsernameRectangleSerializer(data=rect, many=True)
            if (ser.is_valid()):
                print ('heeeh')
                # print (ser.data)
            else:
                print (':(((')

            rect1 = []
            # Save rectangles of the tags of texts
            for obj in enumerate(text_tag):
                temp = {'width': obj[1]['width'],
                        'length': obj[1]['length'],
                        'xCoordinate': obj[1]['xCoordinate'],
                        'yCoordinate': obj[1]['yCoordinate'],
                        'tag_text': id_text}
                rect1.append(temp)
            ser = TagTextRectangleSerializer(data=rect1, many=True)
            if (ser.is_valid()):
                print ('heeeh tany')
                # print (ser.data)
            else:
                print (':((( tany')
                # print (ser.errors)

            # print (rect1)
            return Response({'status': 1})
        else:
            return Response({'status': -1,
                            'username errors': serializer_username_tag.errors,
                            'text errors': serializer_text_tag.errors
                            })


class getUsername(APIView):
    def get(self, request):
        q = request.GET.get("q")
        # icontains acts as LIKE in sql, icontains is case insensitive
        search = User.objects.filter(username__icontains=q).values_list('username')
        print (search)
        text = {'results': list(search)}
        print (text)
        return Response(text)

class getTextTag(APIView):
	def get(self, request):
		q = request.GET.get("q")
		search = Tag.objects.filter(tag__icontains=q).values_list('tag', flat=True).distinct()
		print (search)

		text = {'results': list(search)}
		print (text)
		return Response(text)

class MyPhotosFolder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        query = TagText.objects.filter(user=user_id)
        # print (query)
        print (type(query.values('tag__tag')))
        for q in range(len(query)):
            for i in query.values('tag__tag')[q]:
                # print (q)
                print (i.values)
                print (i)
        results = []
        for q in query:
            results.append({'text_tag': query.values('tag__tag')})
                            # 'image': query.image})
            # print (query.values('tag__tag'))
            # print (q.image)
        print (results)
        # print (images)
        # t = TagText.objects.filter(image__image=images[0])
        # tags = []
        # for i in range(images.count()):
        #     tags.append(TagText.objects.filter(image__image=images[i]))
        # print (tags)

        images_url = []

        # for image in images:
        #     images_url.append(image.image.url)
        # # print (images_url)

        return Response({"images": images_url})

class photosOfMe(APIView):
    def get(self,request):
        username = request.user.username
        images = TagUsername.objects.filter(tag=username)
        # Join query
        images = Image.objects.filter(tagusername__tag=user_id)

        images_url = []

        for image in images:
            images_url.append(image.url)

        return Response(images_url)
