# Generated by Django 2.0.3 on 2018-04-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.IntegerField(choices=[(1, 'Вопрос без вариантов ответа'), (2, 'Вопрос с одним вариантом ответа'), (3, 'Вопрос с несколькими вариантами ответа')], default=2, verbose_name='Тип вопрос'),
        ),
    ]
