from django.conf.urls import url
from User import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

	url(r'^login/?$', views.Login().as_view()),
	url(r'^signup/?$', views.Signup().as_view()),
	url(r'^logout/?$', views.Logout().as_view()),
	url(r'^trail/?$', views.ImageUpload().as_view())

]
urlpatterns = format_suffix_patterns(urlpatterns)	#no need