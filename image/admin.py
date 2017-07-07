from django.contrib import admin
from image.models import Image, Tag, TagText, TagUsername, TagUsernameRectangle, TagTextRectangle

# Register your models here.


class TagTextAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image', 'user']

admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(TagText, TagTextAdmin)
admin.site.register(TagUsername)
admin.site.register(TagUsernameRectangle)
admin.site.register(TagTextRectangle)
