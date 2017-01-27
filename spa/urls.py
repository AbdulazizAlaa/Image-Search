from django.conf.urls import url
from spa import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

# Temporarily disabled
urlpatterns = [

	url(r'^$', views.homePage().as_view())

]