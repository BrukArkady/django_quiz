# Generated by Django 2.0.3 on 2018-03-23 14:09

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20180323_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rightvariant',
            name='variant',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='question', chained_model_field='question', on_delete=django.db.models.deletion.CASCADE, to='main.Variant'),
        ),
    ]