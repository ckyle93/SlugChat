# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commenting', '0002_auto_20160530_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
