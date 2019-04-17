# Generated by Django 2.2 on 2019-04-17 00:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_temporary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='temporary',
            options={'verbose_name': '紐づけデータ', 'verbose_name_plural': '紐づけデータ'},
        ),
        migrations.AlterField(
            model_name='temporary',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID'),
        ),
    ]
