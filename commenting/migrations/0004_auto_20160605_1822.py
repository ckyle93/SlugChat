# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 01:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commenting', '0003_auto_20160602_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
