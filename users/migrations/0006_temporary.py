# Generated by Django 2.2 on 2019-04-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190412_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idm', models.BigIntegerField(unique=True, verbose_name='FeliCa ID')),
                ('uuid', models.UUIDField(verbose_name='UUID')),
            ],
        ),
    ]
