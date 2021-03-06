# Generated by Django 2.0.3 on 2018-04-04 08:40

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0039_auto_20180404_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата и время прохорждения тестирования')),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Результат')),
                ('percent_result', models.IntegerField(verbose_name='Процент правильных ответов')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Questionnaire', verbose_name='Вопросника')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователя')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
    ]
