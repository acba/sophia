# Generated by Django 3.0.10 on 2021-02-10 19:49

import apps.docs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_auto_20210209_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processedtext',
            name='file_wc',
            field=models.FileField(upload_to=apps.docs.models.docs_wc_directory_path, verbose_name='Wordcloud'),
        ),
    ]