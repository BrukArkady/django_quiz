# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_variant_is_right_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_num',
            field=models.IntegerField(default=2, verbose_name='Number of question'),
            preserve_default=False,
        ),
    ]