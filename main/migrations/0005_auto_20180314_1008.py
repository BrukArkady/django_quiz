# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-14 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180314_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='questionnaire',
            field=models.CharField(max_length=50),
        ),
    ]
