# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-29 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20161226_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='uploaded_by',
        ),
    ]
