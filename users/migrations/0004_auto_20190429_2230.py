# Generated by Django 2.2 on 2019-04-29 13:30

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190429_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='idm',
            field=users.models.IDmField(unique=True, verbose_name='FeliCa ID'),
        ),
        migrations.AlterField(
            model_name='temporary',
            name='idm',
            field=users.models.IDmField(unique=True, verbose_name='FeliCa ID'),
        ),
    ]
