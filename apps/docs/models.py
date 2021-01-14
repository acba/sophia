from django.db import models

class TextDocument(models.Model):
    nome     = models.CharField('Nome do Documento', max_length=255, blank=True)
    file     = models.FileField('File', upload_to='text/')

    filename = models.CharField('Nome do Arquivo', max_length=255, blank=True)
    size     = models.BigIntegerField('Tamanho Arquivo', null=True)
    mime     = models.CharField('MIME Type', max_length=255, blank=True)
    ext      = models.CharField('Extensão', max_length=255, blank=True)

    data_upload      = models.DateTimeField('Data de Upload', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now=True)

    foi_transcrito = models.BooleanField('Foi Transcrito', default=False)
    transcricao    = models.TextField('Texto Transcrito', default=None, null=True)

    class Meta:
        verbose_name        = "Documento de Texto"
        verbose_name_plural = "Documentos de Texto"
        ordering = ('data_upload',)

    def __str__(self):
        return self.nome[:50]
