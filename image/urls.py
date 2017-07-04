from django.conf.urls import url
from image import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

    url(r'^upload/?$', views.ImageUpload().as_view()),
    url(r'^search/?$', views.RenderImage().as_view()),
    url(r'^tagText/?$', views.AddTag().as_view()),
    url(r'^getUsername/?$', views.getUsername().as_view()),
    url(r'^face/?$', views.FaceDetection().as_view()),
    url(r'^getTextTag/?$', views.getTextTag().as_view()),
    url(r'^myphotos/?$', views.MyPhotosFolder().as_view()),
    url(r'^photosOfMe/?$', vies.photosOfMe().as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)  # no need
