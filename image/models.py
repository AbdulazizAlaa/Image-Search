from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
import uuid

class Tag(models.Model):
    tag = models.CharField(max_length=225, blank=True, unique=True)

    # class Meta:
    #     unique_together = ('tag')
    def __str__(self):
        return self.tag

# my_upload_to method to change the image title
def my_upload_to(instance, filename):
    # "instance" is an instance of Image
    # split the image extension
    name, extension = os.path.splitext(filename)

    # return a path here, with adding the image extension
    return 'user_{0}'.format(instance.uploaded_by.id) + '/' + str(uuid.uuid4()) + extension

class Image(models.Model):
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by', on_delete=models.PROTECT)
    image = models.ImageField(upload_to=my_upload_to)
    caption = models.TextField(blank=True)
    def __unicode__(self):
        return os.path.basename(self.image.name)


class TagText(models.Model):
    # the tag is a text
    name = models.ManyToManyField(Tag, related_name='tag_text')
    image = models.ForeignKey(Image)

    # # Detection Rectangle specs(width,height, coordinate x & coordinate y)
    w = models.FloatField(blank=True, null=True)
    h = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)

    # who added this tag
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class TagUsername(models.Model):
    # the tag is person
    name = models.ManyToManyField(User, related_name='tag_username')
    image = models.ForeignKey(Image)

    # # De tection Rectangle specs(width,height, coordinate x & coordinate y)
    w = models.FloatField(blank=True, null=True)
    h = models.FloatField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)

    # who added this tag
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     tag1 = ", ".join(str(seg) for seg in self.tag.all())
    #     print (tag1)
    #     return (self.user)
    def __str__(self):
        return '{}'.format(self.name)
