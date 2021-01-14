from django.db import models

class AudioDocument(models.Model):
    nome     = models.CharField('Nome do Áudio', max_length=255, blank=True)
    doc      = models.FileField('File', upload_to='audio/')
    filename = models.CharField('Nome do Arquivo', max_length=255, blank=True)
    mime     = models.CharField('MIME Type', max_length=255, blank=True)
    ext      = models.CharField('Extensão', max_length=255, blank=True)

    data_upload      = models.DateTimeField('Data de Upload', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)

    foi_transcrito = models.BooleanField('Foi Transcrito', default=False)
    transcricao    = models.TextField('Texto Transcrito', default=None, null=True)
    class Meta:
        verbose_name        = "Documento de Audio"
        verbose_name_plural = "Documentos de Audio"
        ordering = ('data_upload',)

    def __str__(self):
        return self.nome[:50]

class TextoTranscrito(models.Model):
    transcricao    = models.TextField('Texto Transcrito', default=None, null=True)
    class Meta:
        verbose_name        = "Texto Transcrito"
        verbose_name_plural = "Textos Transcritos"
        ordering = ('transcricao',)

    def __str__(self):
        return self.transcricao[:50]
