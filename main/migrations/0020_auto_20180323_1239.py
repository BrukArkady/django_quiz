# Generated by Django 2.0.3 on 2018-03-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20180323_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rightvariant',
            name='variant',
        ),
        migrations.AddField(
            model_name='rightvariant',
            name='variant',
            field=models.ForeignKey(default=1, on_delete='cascade', to='main.Variant'),
            preserve_default=False,
        ),
    ]
