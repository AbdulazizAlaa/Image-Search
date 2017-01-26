# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-25 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import image.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=image.models.my_upload_to),
        ),
    ]
