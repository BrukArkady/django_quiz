# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20180315_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_num',
            field=models.PositiveIntegerField(verbose_name='Number of question'),
        ),
    ]