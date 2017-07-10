from django.conf.urls import url
from image import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

    url(r'^upload/?$', views.ImageUpload().as_view()),
    url(r'^search/?$', views.RenderImage().as_view()),
    url(r'^tagText/?$', views.AddTag().as_view()),
    url(r'^suggestions/?$', views.getSuggestions().as_view()),
    url(r'^myphotos/?$', views.MyPhotosFolder().as_view()),
    url(r'^photosOfMe/?$', views.photosOfMe().as_view()),
    url(r'^myphotosmob/?$', views.MyPhotosMob().as_view()),
    url(r'^photosofmemob/?$', views.PhotosOfMeMob().as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)  # no need
