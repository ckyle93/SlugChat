# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_user_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(blank=True, default='N/A', max_length=200, null=True),
        ),
    ]
