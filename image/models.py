from __future__ import unicode_literals
from django.db import models
from User.models import User

class Image(models.Model):
	uploaded_by = models.ForeignKey(User)
	image = models.ImageField(upload_to = "images/")

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