from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from User.serializers import UserDataSerializer
from rest_framework.views import APIView
from rest_framework import generics
from User.models import UserData
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class Signup(APIView):
	def post(self, request, format = None):
		serializer = UserDataSerializer(data = request.data)
		if(serializer.is_valid()):
			user = User.objects.create_user(
				serializer.data['username'],
				serializer.data['email'],
				serializer.data['password']
				)
			#add the name because it is not with create_user method
			user.name = serializer.data['name']
			user.save()
			login(request, user)
			print ("logged")
			text = {'valid' : True , 'errors' :"ur password"+serializer.data['password']}
			return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		
		if user is not None:
			login(request, user)
			serializer = UserDataSerializer(user)
			#get rest of the data, in our case the name
			x = self.request.user
			text = {"valid": True, "errors": "none"}
			return Response(text, status=status.HTTP_302_FOUND)
		else:
			text = {'valid' : False , 'errors' : "Invalid Username or Password"}
			return Response(text, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
	def get(self, request):
		logout(request)
		return Response({"valid": True}, status=status.HTTP_200_OK)
