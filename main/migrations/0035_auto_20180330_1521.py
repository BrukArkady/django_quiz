# Generated by Django 2.0.3 on 2018-03-30 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20180329_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='questionnaire',
        ),
        migrations.RemoveField(
            model_name='results',
            name='user',
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]
