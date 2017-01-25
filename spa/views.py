from django.shortcuts import render
from rest_framework import permissions

#single page app view
class homePage(object):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	
	def get(self, Request):
		TemplateView.as_view(template_name='spa/index.html')