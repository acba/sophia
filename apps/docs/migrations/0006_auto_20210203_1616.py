# Generated by Django 3.0.10 on 2021-02-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0005_auto_20210119_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textdocument',
            name='file',
            field=models.FileField(upload_to='text/', verbose_name='Arquivo'),
        ),
        migrations.AlterField(
            model_name='textdocument',
            name='nome',
            field=models.CharField(blank=True, max_length=255, verbose_name='Descrição do Documento'),
        ),
    ]