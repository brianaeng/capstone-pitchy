# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitchy', '0020_auto_20170116_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(upload_to=b''),
        ),
    ]
