# Generated by Django 3.0.10 on 2021-01-19 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiodocument',
            name='foi_transcrito',
        ),
        migrations.AddField(
            model_name='audiodocument',
            name='foi_processado',
            field=models.BooleanField(default=False, verbose_name='Foi Processado'),
        ),
    ]
