from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
import uuid
from User.models import User

class Tag(models.Model):
	tag = models.CharField(max_length= 1000, blank=True)
	def __str__(self):
		return self.tag

#my_upload_to method to change the image title
def my_upload_to(instance, filename):
	# "instance" is an instance of Image
	#split the image extension
	name, extension = os.path.splitext(filename)

	# return a path here, with adding the image extension
	return 'images/' + str(uuid.uuid4()) + extension

class Image(models.Model):
# Generating unique_id for each image field, to call it in the image URL
	# unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

	# Imagefield to track image path
	image = models.ImageField(upload_to = my_upload_to)
	# Tags will track the many to many relationship with images
	# related_name is the name of the relationship in the images model (ie it is the inverse relationship)
	# Tags = models.ManyToManyField(Tag, related_name = 'Images')

	uploaded_by = models.ForeignKey(User, related_name='uploaded_by', on_delete = models.PROTECT)
	# user = models.ManyToManyField(User)
	# user = models.ManyToManyField(UserData, on_delete=models.v, blank=False)
		# def __str__(self):
		# 	return self.user.username
	def __unicode__(self):
	    return os.path.basename(self.image.name)
	# filename = models.CharField(max_length=1000)

class TagText(models.Model):
#the tag is a text
	tag = models.ManyToManyField(Tag, related_name='tag_text')
	image = models.ForeignKey(Image)

	#Detection Rectangle specs(width,height, coordinate x & coordinate y)
	width = models.DecimalField(max_digits=2, decimal_places=2)
	length = models.DecimalField(max_digits=2,decimal_places=2)
	xCoordinate = models.DecimalField(max_digits=2,decimal_places=2)
	yCoordinate = models.DecimalField(max_digits=2,decimal_places=2)

	#who added this tag
	user = models.ForeignKey(User)
	def __str__(self):
		return '{}'.format(self.tag)

class TagUsername(models.Model):
#the tag is person
	tag = models.ManyToManyField(User, related_name='tag_username')
	image = models.ForeignKey(Image)

	#Detection Rectangle specs(width,height, coordinate x & coordinate y)
	width = models.DecimalField(max_digits=2, decimal_places=2)
	length = models.DecimalField(max_digits=2,decimal_places=2)
	xCoordinate = models.DecimalField(max_digits=2,decimal_places=2)
	yCoordinate = models.DecimalField(max_digits=2,decimal_places=2)

	#who added this tag
	user = models.ForeignKey(User)
	def __str__(self):
		return '{}'.format(self.tag)
