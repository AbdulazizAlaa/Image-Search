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

            engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                                'face_recognition': 'facenet',
                                                'object_detection_recognition': 'inception',
                                                'captions_generation_engine': True})

            results = engine.processImage(image_data)

            objects = results['objects']
            faces = results['faces']
            caption = results['captions']

            # objects = ['backpack', 'backpack1', 'back pack', 'knapsack', 'packsack', 'rucksack', 'haversack']
            # caption = "random caption for random image"
            # faces = {}
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
                    tag_text_obj.name.add(tag_obj)
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
            # tags = NER.solve(text)
            tags = ["random", "nada", "backpack"]

            for tag in tags:
                params.append({'tag': tag})
        else:
            # call Arabic model...
            # arabic_model = ANER.ANER()
            # tags = arabic_model.solve(text)
            tags = ["arabic_name", "arabic_name", "arabic_name"]

            for tag in tags:
                params.append({'tag': tag})
        query = []
        output = {}
        # print (tags)
        from django.db.models import Q
        import functools

        # captions search
        query.append(Image.objects.filter(functools.reduce(lambda x, y: x | y, [Q(caption__icontains=word) for word in tags]),
                    uploaded_by=user_id).distinct().values_list('image', 'caption', 'id'))
        # for query in images:
        #     for e in query:
        #         print (e.tag)
        # tag texts search
        query.append((Image.objects.filter(functools.reduce(lambda x, y: x | y, [Q(tagtext__name__tag=word) for word in tags]),
                                        uploaded_by=user_id).distinct()).values_list('image',
                                                                                    'caption',
                                                                                    'id'))
        # # search in tag username
        query.append((Image.objects.filter(functools.reduce(lambda x, y: x | y, [Q(tagusername__name__username=word) for word in tags]),
                                        uploaded_by=user_id).distinct()).values_list('image',
                                                                                    'caption',
                                                                                    'id'))
        print (query)
        images = []
        temp = []
        for image in query:
            for i in image:
                temp.append(i[0])
        temp = set(temp)
        print (temp)
        for i in temp:
            print (i)
            images.append(Image.objects.filter(image=i).values_list('image',
                                                                    'caption',
                                                                    'id'))
        faces = []
        objects = []
        for query in images:
            for image in query:
                url = image[0]
                tag_usernames = TagUsername.objects.filter(image__id=image[2]).values_list('name__username',
                                                                                        'w',
                                                                                        'h',
                                                                                        'x',
                                                                                        'y')
                tag_texts = TagText.objects.filter(image__id=image[2]).values_list('name__tag',
                                                                                'w',
                                                                                'h',
                                                                                'x',
                                                                                'y')
                for t in tag_usernames:
                    faces.append({'names': t[0],
                                'w': t[1],
                                'h': t[2],
                                'x': t[3],
                                'y': t[4],
                                'user_flag': True})
                for t in tag_texts:
                    if t[1] is None and t[2] is None and t[3] is None and t[4] is None:
                        objects.append(t[0])
                    else:
                        # print ('ylawhy')
                        faces.append({'name': t[0],
                                    'w': t[1],
                                    'h': t[2],
                                    'x': t[3],
                                    'y': t[4],
                                    'user_flag': False})
                    if url not in output:
                        output[url] = []
                    temp = {
                        'faces': faces,
                        'caption': image[1],
                        'objects': objects}
                output[url].append(temp)
                # print (faces)
                # print (tag_usernames)
        #         output.append(image.image.url)
        # # print (i)
        # print (output)
        # print (set(output))
        return Response(output)

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
            image_name = image_obj.image.name
            image_file = image_obj.image.url
        except:
            return Response({'status':-1, 'data':'Image Not Found'})

        # image object
        image_data = cv2.imread(image_file)

        # getting actual persons rectangles based on user_flag
        user_tag_rect = []

        # TAG TEXT
        # saving tags and linking them to image
        for tag_obj_str in text_tag:
            tag_text_obj = TagText.objects.create(image=image_obj,
                                                user=user_obj,
                                                h=tag_obj_str['h'],
                                                w=tag_obj_str['w'],
                                                y=tag_obj_str['y'],
                                                x=tag_obj_str['x'])
            tag_serializer = TagSerializer(data={'tag': tag_obj_str['name']})
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
                tag_obj = Tag.objects.filter(tag=tag_obj_str['name']).first()
                # print('-------------')
                # print('object')
                # print(tag_obj)
                # adding the tag to image
                tag_text_obj.name.add(tag_obj)

                tag_obj_str['name'] = tag_obj_str['name']+"_0"
                user_tag_rect.append(tag_obj_str)
            except Tag.DoesNotExist:
                print ("Tag does not exist")
                pass

        # TAG username
        # saving tags and linking them to image
        for tag_obj_str in username_tag:

            # getting the tag object and then associate with image
            try:
                tagged_user = User.objects.get(username=tag_obj_str['name'])
                tag_username_obj = TagUsername.objects.create(image=image_obj,
                                                            user=user_obj,
                                                            h=tag_obj_str['h'],
                                                            w=tag_obj_str['w'],
                                                            y=tag_obj_str['y'],
                                                            x=tag_obj_str['x'])

                # adding the tag to image
                tag_username_obj.name.add(tagged_user)

                tag_obj_str['name'] = tag_obj_str['name']+"_1"
                user_tag_rect.append(tag_obj_str)
            except:
                print ("user does not exist")
                pass

        # creating engine instance
        engine = vision_engine.VisionEngine({'face_detection': 'MTCNN_engine',
                                            'face_recognition': 'facenet',
                                            'object_detection_recognition': False,
                                            'captions_generation_engine': False})

        print(user_tag_rect)
        # is used after Successfully tagging image by user so it can be used for training
        engine.store_face_training_data(image_data, user_tag_rect, image_name)

        return Response({'status':1})


class getSuggestions(APIView):
    def get(self, request):
        q = request.GET.get("q")
        # icontains acts as LIKE in sql, icontains is case insensitive
        search = []
        usernames = User.objects.filter(username__icontains=q).values_list('username')
        texts = Tag.objects.filter(tag__icontains=q).values_list('tag')
        print ((usernames))
        for name in usernames:
            search.append({'name': name[0], 'user_flag': True})
        for name in texts:
            search.append({'name': name[0], 'user_flag': False})

        print (search)
        text = {'suggestions': search}
        return Response(text)


class MyPhotosFolder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        ####################################################text tags:###################################
        q = TagText.objects.filter(user=user_id).values_list('name__tag',
                                                            'image__image',
                                                            'name__id',
                                                            'w',
                                                            'h',
                                                            'x',
                                                            'y',
                                                            'image__id',
                                                            'image__caption').distinct()
        # print (q)
        albums = {}
        for i in q:
            tag = i[0]
            image_url = i[1]
            # Get all tags of this image
            tags_text = TagText.objects.filter(image__id=i[7]).values_list('name__tag', 'w', 'h', 'x', 'y')
            # print (tags_text)
            # Get all tags of this image
            tags_username = TagUsername.objects.filter(image__id=i[7]).values_list('name__username', 'w', 'h', 'x', 'y')
            faces = []
            objects = []
            for t in tags_text:
                if t[1] is None and t[2] is None and t[3] is None and t[4] is None:
                    objects.append(t[0])
                else:
                    # print ('ylawhy')
                    faces.append({'name': t[0],
                                'w': t[1],
                                'h': t[2],
                                'x': t[3],
                                'y': t[4],
                                'user_flag': False})
            for t in tags_username:
                # print ('ylawhy')
                faces.append({'name': t[0],
                            'w': t[1],
                            'h': t[2],
                            'x': t[3],
                            'y': t[4],
                            'user_flag': True})
            if tag not in albums:
                albums[tag] = []
            temp = {'url': image_url,
                    'faces': faces,
                    'caption': i[8],
                    'objects': objects}
            albums[tag].append(temp)
        # print (albums)

        ##########################################username tags###########################################
        q = TagUsername.objects.filter(user=user_id, ).values_list('name__username',
                                                            'image__image',
                                                            'name__id',
                                                            'w',
                                                            'h',
                                                            'x',
                                                            'y',
                                                            'image__id',
                                                            'image__caption').distinct()
        print (q)
        for i in q:
            tag = i[0]
            image_url = i[1]
            # Get all tags of this image
            tags_text = TagText.objects.filter(image__id=i[7]).values_list('name__tag', 'w', 'h', 'x', 'y')
            # print (tags_text)
            # Get all tags of this image
            tags_username = TagUsername.objects.filter(image__id=i[7]).values_list('name__username', 'w', 'h', 'x', 'y')
            print (tags_username)
            faces = []
            objects = []
            for t in tags_text:
                if t[1] is None and t[2] is None and t[3] is None and t[4] is None:
                    objects.append(t[0])
                else:
                    print ('ylawhy')
                    faces.append({'name': t[0],
                                'w': t[1],
                                'h': t[2],
                                'x': t[3],
                                'y': t[4],
                                'user_flag': False})
            for t in tags_username:
                print ('ylawhy')
                faces.append({'name': t[0],
                            'w': t[1],
                            'h': t[2],
                            'x': t[3],
                            'y': t[4],
                            'user_flag': True})
            if tag not in albums:
                albums[tag] = []
            temp = {'url': image_url,
                    'faces': faces,
                    'caption': i[8],
                    'objects': objects}
            albums[tag].append(temp)
        # print (albums)
        return Response(albums)


class photosOfMe(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        username = request.user.id
        print (request.user.username)
        q = TagUsername.objects.filter(name=username).values_list('user__username',
                                                            'image__image',
                                                            'name__id',
                                                            'w',
                                                            'h',
                                                            'x',
                                                            'y',
                                                            'image__id',
                                                            'image__caption')
        print (q)
        # Join query
        # images = Image.objects.filter(tagusername__tag=user_id)
        albums = {}
        for i in q:
            tag = i[0]
            image_url = i[1]
            # Get all tags of this image
            tags_text = TagText.objects.filter(image__id=i[7]).values_list('name__tag', 'w', 'h', 'x', 'y')
            # print (tags_text)
            # Get all tags of this image
            tags_username = TagUsername.objects.filter(image__id=i[7]).values_list('name__username', 'w', 'h', 'x', 'y')
            print (tags_username)
            faces = []
            objects = []
            for t in tags_text:
                if t[1] is None and t[2] is None and t[3] is None and t[4] is None:
                    objects.append(t[0])
                else:
                    print ('ylawhy')
                    faces.append({'name': t[0],
                                'w': t[1],
                                'h': t[2],
                                'x': t[3],
                                'y': t[4],
                                'user_flag': False})
            for t in tags_username:
                print ('ylawhy')
                faces.append({'name': t[0],
                            'w': t[1],
                            'h': t[2],
                            'x': t[3],
                            'y': t[4],
                            'user_flag': True})
            if tag not in albums:
                albums[tag] = []
            temp = {'url': image_url,
                    'faces': faces,
                    'caption': i[8],
                    'objects': objects}
            albums[tag].append(temp)
        return Response(albums)
