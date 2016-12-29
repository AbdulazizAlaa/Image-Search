from django.contrib.auth.models import User
from django.contrib import admin
import os
from urlparse import urlparse
from uuid import uuid4
from User.models import User

# Create your models here.
class Image(models.Model):
	# def path_and_rename(path):
	#     def wrapper(instance, filename):
	#         ext = filename.split('.')[-1]
	#         # get filename
	#         if instance.pk:
	#             filename = '{}.{}'.format(instance.pk, ext)
	#         else:
	#             # set filename as random string
	#             filename = '{}.{}'.format(uuid4().hex, ext)
	#         # return the whole path to the file
	#         return os.path.join(path, filename)
	#     return wrapper
	image = models.ImageField(upload_to = "images/")
	# uploaded_by = models.ForeignKey(User, null = True)
	# user = models.ManyToManyField(User)
	# user = models.ManyToManyField(UserData, on_delete=models.v, blank=False)
		# def __str__(self):
		# 	return self.user.username
	def __unicode__(self):
	    return os.path.basename(self.image.name)
	# filename = models.CharField(max_length=1000)




class Tag(models.Model):
	tag_text = models.CharField(max_length=500)
	image = models.ForeignKey(Image)
	imageRelation = models.ManyToManyField(Image, related_name = 'tags')

	@api_view(['GET', 'POST'])
	def get_image(self, request, aid):
		try:
			image = Tag.objects.filter(tag_text=aid)
		except image.DoesNotExist :
			raise Error404

		serializer = ImageSerializer(image)
		return Response(serializer.data)
