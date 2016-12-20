from django.shortcuts import render
<<<<<<< HEAD

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from User.serializers import UserDataSerializer, ImageSerializer
from rest_framework.views import APIView
from rest_framework import generics
from User.models import UserData,Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.renderers import TemplateHTMLRenderer

=======
from rest_framework.response import Response
from rest_framework import status
from User.serializers import UserDataSerializer
from rest_framework.views import APIView
from rest_framework import generics
from User.models import UserData
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
class Signup(APIView):
	def post(self, request, format = None):
		serializer = UserDataSerializer(data = request.data)
		if(serializer.is_valid()):
			user = User.objects.create_user(
				username = serializer.data['username'],
				first_name = serializer.data['first_name'],
				last_name = serializer.data['last_name'],
				email = serializer.data['email'],
				password = serializer.data['password'],
				)
			#add the name because it is not with create_user method
			# user.name = serializer.data['name']
			# user.save()
<<<<<<< HEAD
			login(request, user)
			print ("logged")
			text = {'valid' : True , 'errors' :"ur password"+serializer.data['password']}
			return JsonResponse(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

=======
			return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
class Login(APIView):
	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
<<<<<<< HEAD
		
		if user is not None:
			login(request, user)
			serializer = UserDataSerializer(user)
			return JsonResponse(serializer.data, status=status.HTTP_302_FOUND)
=======
		if user is not None:
			serializer = UserDataSerializer(user)
			#get rest of the data, in our case the name
			temp = self.request.user
			text = {"valid": True, "errors": ""}
			return Response(serializer.data, status=status.HTTP_302_FOUND)
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
		else:
			text = {'valid' : False , 'errors' : "Invalid Username or Password"}
			return Response(text, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
	def get(self, request):
		logout(request)
		return Response({"valid": True}, status=status.HTTP_200_OK)
<<<<<<< HEAD

class ImageUpload(generics.CreateAPIView):

	queryset = Image.objects.all()
	serializer_class = ImageSerializer
=======
>>>>>>> 9d0ef3abd9c3e2c5e391802f1debbacaf9eaff5e
