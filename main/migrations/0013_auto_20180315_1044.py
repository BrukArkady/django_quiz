# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_question_question_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_num',
            field=models.IntegerField(unique=True, verbose_name='Number of question'),
        ),
    ]
