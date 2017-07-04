"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
admin.autodiscover()

schema_view = get_swagger_view(title='Image Search API')

urlpatterns = [
    # Matches the root route (Our landing page)
    url(r'^$', TemplateView.as_view(template_name='landing/index.html')),
    # Matches our SPA root
    url(r'^home/', include('spa.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('User.urls')),
    url(r'^image/', include('image.urls')),
   	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    # For API documentation(DRF)
    # url(r'^docs/', include('rest_framework_docs.urls')),
    # url(r'^api/', include('api.urls', namespace="documentation")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

# I added this route to catch any failing routes, this is a hack
# to pass routes that were not found by Django to React, this
# way we can be sure if a user enters a link that is handled
# by React's router that Django will not block the user's
# request.
urlpatterns.append(url(r'^.*', TemplateView.as_view(template_name='spa/index.html')))
