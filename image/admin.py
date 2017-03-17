from django.contrib import admin
from image.models import Image, Tag, TagText, TagUsername
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(TagText)
admin.site.register(TagUsername)

# Register your models here.
