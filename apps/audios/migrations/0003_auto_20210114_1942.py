# Generated by Django 3.0.10 on 2021-01-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audios', '0002_auto_20210113_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=255, verbose_name='Nome do Documento')),
                ('file', models.FileField(upload_to='text/', verbose_name='File')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='Nome do Arquivo')),
                ('mime', models.CharField(blank=True, max_length=255, verbose_name='MIME Type')),
                ('ext', models.CharField(blank=True, max_length=255, verbose_name='Extensão')),
                ('data_upload', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('foi_transcrito', models.BooleanField(default=False, verbose_name='Foi Transcrito')),
                ('transcricao', models.TextField(default=None, null=True, verbose_name='Texto Transcrito')),
            ],
            options={
                'verbose_name': 'Documento de Texto',
                'verbose_name_plural': 'Documentos de Texto',
                'ordering': ('data_upload',),
            },
        ),
        migrations.AlterModelOptions(
            name='audiodocument',
            options={'ordering': ('data_upload',), 'verbose_name': 'Documento de Audio', 'verbose_name_plural': 'Documentos de Audio'},
        ),
        migrations.AddField(
            model_name='audiodocument',
            name='ext',
            field=models.CharField(blank=True, max_length=255, verbose_name='Extensão'),
        ),
        migrations.AddField(
            model_name='audiodocument',
            name='filename',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome do Arquivo'),
        ),
        migrations.AddField(
            model_name='audiodocument',
            name='mime',
            field=models.CharField(blank=True, max_length=255, verbose_name='MIME Type'),
        ),
        migrations.AlterField(
            model_name='audiodocument',
            name='data_atualizacao',
            field=models.DateTimeField(auto_now=True, verbose_name='Data de Atualização'),
        ),
        migrations.AlterField(
            model_name='audiodocument',
            name='doc',
            field=models.FileField(upload_to='audio/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='audiodocument',
            name='foi_transcrito',
            field=models.BooleanField(default=False, verbose_name='Foi Transcrito'),
        ),
        migrations.AlterField(
            model_name='audiodocument',
            name='nome',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome do Áudio'),
        ),
    ]