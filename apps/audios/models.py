from django.db import models

class AudioDocument(models.Model):
    nome = models.CharField(max_length=255, blank=True)
    doc = models.FileField(upload_to='audio/')

    data_upload = models.DateTimeField('Data de Upload', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now_add=True)

    foi_transcrito = models.BooleanField(default=False)
    transcricao = models.TextField(default=None, null=True)

    class Meta:
        verbose_name        = "Audio"
        verbose_name_plural = "Audios"
        ordering = ('data_upload',)

    def __str__(self):
        return self.nome[:50]
