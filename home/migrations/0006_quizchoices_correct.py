# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-25 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20160522_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizchoices',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]