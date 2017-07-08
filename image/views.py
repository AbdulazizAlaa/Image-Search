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
import re
# from engine.nlp.ner import NER
# from engine.nlp.aner import ANER
from rest_framework import permissions

from engine.cv.vision import vision_engine

import numpy as np
import cv2


class ImageUpload(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        print(request.data)
        image = request.data.get('image')
        uploaded_by = request.user.username
        user_obj = request.user

        myjson = {'image': image, 'uploaded_by': uploaded_by}

        serializer = ImageUploadSerializer(data=myjson)
        if serializer.is_valid():
            serializer.save()

            serializer_obj = serializer.data
            print (serializer_obj)

            image_file = serializer_obj['image']

            image_obj = Image.objects.get(id=serializer_obj['id'])

            image_data = cv2.imread(image_file)

            # engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
            #                                     'face_recognition': 'facenet',
            #                                     'object_detection_recognition': 'inception',
            #                                     'captions_generation_engine': True})

            # results = engine.processImage(image_data)

            # objects = results['objects']
            # faces = results['faces']
            # caption = results['captions']

            objects = ['backpack', 'backpack1', 'back pack', 'knapsack', 'packsack', 'rucksack', 'haversack']
            caption = "random caption for random image"
            faces = {}
            print ('objects', objects)
            print('faces', faces)
            print('caption', caption)

            # saving tags and linking them to image
            for tag_str in objects:
                # tag text object creation
                tag_text_obj = TagText.objects.create(image=image_obj, user=user_obj)
                # tag object creation
                tag_serializer = TagSerializer(data={'tag': tag_str})
                if(tag_serializer.is_valid()):
                    try:
                        tag_serializer.save()
                    except:
                        # tag is already saved
                        # print('-------------')
                        # print ("exception: ")
                        pass

                # getting the tag object and then associate with image
                try:
                    # getting the tag object
                    tag_obj = Tag.objects.filter(tag=tag_str).first()
                    # print('-------------')
                    # print('object')
                    # print(tag_obj)
                    # adding the tag to image
                    tag_text_obj.tag.add(tag_obj)
                except Tag.DoesNotExist:
                    print ("NO")
                    pass

            # adding caption to image object
            image_obj_temp = {'caption': caption}
            serializer_temp = ImageUploadSerializer(image_obj, data=image_obj_temp, partial=True)
            if serializer_temp.is_valid():
                serializer_temp.save()

                serializer_obj_temp = serializer_temp.data
                print (serializer_obj_temp)

            image_obj = Image.objects.get(id=serializer_obj['id'])

            result = {'image_id': serializer_obj['id'],
                    'url': image_obj.image.url,
                    'caption': caption,
                    'objects': objects,
                    'faces': faces}

            print('image', result)

            text = {'status': 1, 'image': result}
            return Response(text)
        else:
            text = {'status': -1, 'image': serializer.errors}
            return Response(text)


class RenderImage(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user_id = request.user.id
        # print (user_id)
        text = request.GET.get("q")
        
        language = ""

        eng_matches = re.findall(pattern="([a-z]|[A-Z]|[0-9])", string=text)

        if(len(eng_matches) > 0.5 * len(text)):
            language = "en"
        else:
            language = "ar"

        # Params of the serializer
        params = []
        if(language != "ar"):
            # Tags = NER.solve(text)
            Tags = ["random", "train", "LINA"]

            for tag in Tags:
                params.append({'tag': tag})
        else:
            # call Arabic model...
            # arabic_model = ANER.ANER()
            # Tags = arabic_model.solve(text)
            Tags = ["arabic_name", "arabic_name", "arabic_name"]

            for tag in Tags:
                params.append({'tag': tag})
        images = []
        output = []
        print (Tags)
        from django.db.models import Q
        # captions search
        images.append(Image.objects.filter(reduce(lambda x, y: x | y, [Q(caption__icontains=word) for word in Tags]),
                    uploaded_by=user_id))#.values_list('image', 'caption', 'tagtext__tag__tag', 'tagusername__tag__username'))
        # for query in images:
        #     for e in query:
        #         print (e.tag)
        # tag texts search
        images.append((Image.objects.filter(reduce(lambda x, y: x | y, [Q(tagtext__tag__tag=word) for word in Tags]),
                                        uploaded_by=user_id).distinct()).values_list('image',
                                                                                    'caption'))
        # # search in tag username
        images.append((Image.objects.filter(reduce(lambda x, y: x | y, [Q(tagusername__tag__username=word) for word in Tags]),
                                        uploaded_by=user_id).distinct()).values_list('image',
                                                                                    'caption'))
        print (images)
        # for query in images:
        #     for image in query:
        #         # print (image)
        #         output.append(image.image.url)
        # # print (i)
        # print (output)
        # print (set(output))
        return Response({'images': set(output)})
        

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
        user_obj = request.user
        text_tag = request.data.get("tag_text")
        username_tag = request.data.get("tag_username")
        image_id = request.data.get("image")
        try:
            image_obj = Image.objects.get(id=image_id)
        except:
            return Response({'status':-1, 'data':'Image Not Found'})

        # # creating engine instance
        # engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
        #                                     'face_recognition': 'facenet',
        #                                     'object_detection_recognition': False,
        #                                     'captions_generation_engine': False})

        # # is used after Successfully tagging image by user so it can be used for training
        # engine.store_face_training_data(img, [{'name': 'aziz', 'x': 424, 'h': 393, 'y': 188, 'w': 313}], "aziz.jpg")


        # TAG TEXT
        # saving tags and linking them to image
        for tag_obj_str in text_tag:
            tag_text_obj = TagText.objects.create(image=image_obj,
                                                user=user_obj,
                                                length=tag_obj_str['length'],
                                                width=tag_obj_str['width'],
                                                yCoordinate=tag_obj_str['yCoordinate'],
                                                xCoordinate=tag_obj_str['xCoordinate'])
            tag_serializer = TagSerializer(data={'tag': tag_obj_str['tag']})
            if(tag_serializer.is_valid()):
                try:
                    tag_serializer.save()
                except Exception as ex:
                    # tag is already saved
                    # print('-------------')
                    # print ("exception: ")
                    # print(ex)
                    pass

            # getting the tag object and then associate with image
            try:
                # getting the tag object
                tag_obj = Tag.objects.filter(tag=tag_obj_str['tag']).first()
                # print('-------------')
                # print('object')
                # print(tag_obj)
                # adding the tag to image
                tag_text_obj.tag.add(tag_obj)
            except Tag.DoesNotExist:
                print ("Tag does not exist")
                pass

        # TAG username
        # saving tags and linking them to image
        for tag_obj_str in username_tag:
            tag_username_obj = TagUsername.objects.create(image=image_obj,
                                                        user=user_obj,
                                                        length=tag_obj_str['length'],
                                                        width=tag_obj_str['width'],
                                                        yCoordinate=tag_obj_str['yCoordinate'],
                                                        xCoordinate=tag_obj_str['xCoordinate'])

            # getting the tag object and then associate with image
            try:
                tagged_user = User.objects.get(username=tag_obj_str['username'])

                # adding the tag to image
                tag_username_obj.tag.add(tagged_user)
            except:
                print ("user does not exist")
                pass

        return Response({'status':1})


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
        # text tags:
        q = TagText.objects.filter(user=user_id).values_list('tag__tag',
                                                            'image__image',
                                                            'tag__id',
                                                            'width',
                                                            'length',
                                                            'xCoordinate',
                                                            'yCoordinate')
        print (q)
        # inst = TagText.objects.filter(pk=rect[0][2]).values_list('tag__tag')
        # print (rect)
        # print (inst)
        # l = rect[0::3]
        # print (l)
        albums = {}
        for i in q:
            tag = i[0]
            image_url = i[1]
            print(tag)
            print(image_url)
            if tag not in albums:
                albums[tag] = []
            temp = {'image_url': image_url,'w': i[3],'h': i[4],'x': i[5],'y': i[6]}
            albums[tag].append(temp)
        print (albums)
        return Response(albums)


class photosOfMe(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        username = request.user.id
        print (username)
        q = TagUsername.objects.filter(tag=username).values_list('tag__username',
                                                            'image__image',
                                                            'tag__id',
                                                            'width',
                                                            'length',
                                                            'xCoordinate',
                                                            'yCoordinate')
        print (q)
        # Join query
        # images = Image.objects.filter(tagusername__tag=user_id)
        albums = {}
        for i in q:
            tag = i[0]
            image_url = i[1]
            print(tag)
            print(image_url)
            if tag not in albums:
                albums[tag] = []
            temp = {'image_url': image_url,'w': i[3],'h': i[4],'x': i[5],'y': i[6]}
            albums[tag].append(temp)
        # print (albums)
        return Response(albums)