# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20161017_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
