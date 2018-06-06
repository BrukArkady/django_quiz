# Generated by Django 2.0.3 on 2018-03-29 12:55

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0032_auto_20180329_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now=True, verbose_name='Дата и время прохорждения тестирования')),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Результат')),
                ('percent_result', models.FloatField(verbose_name='Процент правильных ответов')),
                ('questionnaire', models.ForeignKey(on_delete='cascade', to='main.Questionnaire', verbose_name='Вопросника')),
                ('user', models.ForeignKey(on_delete='cascade', to=settings.AUTH_USER_MODEL, verbose_name='Пользователя')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
    ]
