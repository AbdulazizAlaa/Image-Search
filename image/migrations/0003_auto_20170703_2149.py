# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-03 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_image_caption'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='image',
        #     name='caption',
        #     field=models.TextField(default=''),
        #     preserve_default=False,
        # ),
        migrations.AddField(
            model_name='tagtext',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagtext',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagtext',
            name='xCoordinate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagtext',
            name='yCoordinate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagusername',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagusername',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagusername',
            name='xCoordinate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagusername',
            name='yCoordinate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]