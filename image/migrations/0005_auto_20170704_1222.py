# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-04 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_image_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagUsernameRectangle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.FloatField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('xCoordinate', models.FloatField(blank=True, null=True)),
                ('yCoordinate', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tagusername',
            name='length',
        ),
        migrations.RemoveField(
            model_name='tagusername',
            name='width',
        ),
        migrations.RemoveField(
            model_name='tagusername',
            name='xCoordinate',
        ),
        migrations.RemoveField(
            model_name='tagusername',
            name='yCoordinate',
        ),
        migrations.AddField(
            model_name='tagusernamerectangle',
            name='tag_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.TagUsername'),
        ),
    ]
