from django.conf.urls import url
from image import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

	
	url(r'^trail/?$', views.ImageUpload().as_view()),



]
urlpatterns = format_suffix_patterns(urlpatterns)	#no need