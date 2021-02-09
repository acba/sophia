from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
def audiodoc_directory_path(instance, filename):
    return 'user_{0}/audios/{1}'.format(instance.user.id, filename)

class AudioDocument(models.Model):
    nome = models.CharField('Descrição do Áudio', max_length=255, blank=True)
    file = models.FileField('Arquivo', upload_to=audiodoc_directory_path)
    user = models.ForeignKey('users.User', related_name="audiodocs", on_delete=models.CASCADE, null=False, default=None)

    filename = models.CharField('Nome do Arquivo', max_length=255, blank=True)
    size     = models.BigIntegerField('Tamanho Arquivo', null=True)
    mime     = models.CharField('MIME Type', max_length=255, blank=True)
    ext      = models.CharField('Extensão', max_length=255, blank=True)

    data_upload      = models.DateTimeField('Data de Upload', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)

    foi_processado = models.BooleanField('Foi Processado', default=False)
    class Meta:
        verbose_name        = "Documento de Audio"
        verbose_name_plural = "Documentos de Audio"
        ordering = ('data_upload',)

    def __str__(self):
        return self.nome[:50]

def audiodoc_wc_directory_path(instance, filename):
    return 'user_{0}/audios/{1}'.format(instance.audiodoc.user.id, filename)

class ProcessedAudio(models.Model):
    audiodoc = models.OneToOneField(AudioDocument, related_name='processedaudio', on_delete=models.CASCADE, primary_key=True)
    processor = models.CharField('Processador', max_length=255, blank=True)

    file_wc = models.FileField('Wordcloud', upload_to=audiodoc_wc_directory_path)

    data_criacao     = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now=True)

    class Meta:
        verbose_name        = "Texto Processado"
        verbose_name_plural = "Textos Processados"
        ordering = ('data_criacao',)

    def __str__(self):
        if self.trechos.first() is not None:
            return self.trechos.first().text[:200]
        else:
            return 'Não Reconhecido'

class LegendaTrecho(models.Model):
    pdoc = models.ForeignKey(ProcessedAudio, related_name="trechos", on_delete=models.CASCADE, null=False, default=None)

    start = models.FloatField('Inicio Trecho')
    end   = models.FloatField('Fim Trecho', null=True)
    text  = models.TextField('Texto', default=None, null=True)

    def __str__(self):
        return self.text[:200]

class TermoFreqData(models.Model):
    pdoc = models.ForeignKey(ProcessedAudio, related_name="mais_frequentes", on_delete=models.CASCADE, null=False, default=None)

    termo = models.CharField('Termo', max_length=255, blank=True)
    qtd   = models.IntegerField('Qtd', blank=True)

    def __str__(self):
        return f'{self.termo}: {self.qtd}'


# Whenever ANY model is deleted, if it has a file field on it, delete the associated file too
@receiver(post_delete, sender=AudioDocument)
def delete_audiodoc_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

# Whenever ANY model is deleted, if it has a file field on it, delete the associated file too
@receiver(post_delete, sender=ProcessedAudio)
def delete_processedaudio_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

# Only delete the file if no other instances of that model are using it
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)
