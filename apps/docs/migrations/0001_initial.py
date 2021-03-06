# Generated by Django 3.0.10 on 2021-01-18 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TextDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=255, verbose_name='Nome do Documento')),
                ('file', models.FileField(upload_to='text/', verbose_name='File')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='Nome do Arquivo')),
                ('size', models.BigIntegerField(null=True, verbose_name='Tamanho Arquivo')),
                ('mime', models.CharField(blank=True, max_length=255, verbose_name='MIME Type')),
                ('ext', models.CharField(blank=True, max_length=255, verbose_name='Extensão')),
                ('data_upload', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('foi_transcrito', models.BooleanField(default=False, verbose_name='Foi Transcrito')),
                ('transcricao', models.TextField(default=None, null=True, verbose_name='Texto Transcrito')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='textdocs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Documento de Texto',
                'verbose_name_plural': 'Documentos de Texto',
                'ordering': ('data_upload',),
            },
        ),
        migrations.CreateModel(
            name='ProcessedText',
            fields=[
                ('textdoc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='docs.TextDocument')),
                ('texto', models.TextField(default=None, null=True, verbose_name='Texto Transcrito')),
                ('file_wc', models.FileField(upload_to='wc/', verbose_name='Wordcloud')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Texto Processado',
                'verbose_name_plural': 'Textos Processados',
                'ordering': ('data_criacao',),
            },
        ),
        migrations.CreateModel(
            name='CPFData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=255, verbose_name='cpf')),
                ('pdoc', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='docs.ProcessedText')),
            ],
        ),
    ]
