from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	query_results = User.objects.all()
# Create your views here.
