from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    template = loader.get_template("Hello World")
    return HttpResponse(template.render())