# Generated by Django 2.0.3 on 2018-03-30 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Questionnaire', verbose_name='Название вопросника'),
        ),
        migrations.AlterField(
            model_name='results',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Questionnaire', verbose_name='Вопросника'),
        ),
        migrations.AlterField(
            model_name='results',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователя'),
        ),
        migrations.AlterField(
            model_name='rightvariant',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Question', verbose_name='Вопрос'),
        ),
    ]
