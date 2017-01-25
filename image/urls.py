from django.conf.urls import url
from image import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

	
	url(r'^upload/?$', views.ImageUpload().as_view()),
	url(r'^search/?$', views.RenderImage().as_view()),



]
urlpatterns = format_suffix_patterns(urlpatterns)	#no need
