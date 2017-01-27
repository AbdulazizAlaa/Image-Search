from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from django.views.generic import TemplateView

#single page app view
class homePage(APIView):
	def get(self, Request):
		TemplateView.as_view(template_name='spa/index.html')