from django.db import models

class AudioDocument(models.Model):
    nome = models.CharField('Descrição do Áudio', max_length=255, blank=True)
    file = models.FileField('Arquivo', upload_to='audio/')
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


class ProcessedAudio(models.Model):
    audiodoc = models.OneToOneField(AudioDocument, related_name='processedaudio', on_delete=models.CASCADE, primary_key=True)
    processor = models.CharField('Processador', max_length=255, blank=True)

    file_wc = models.FileField('Wordcloud', upload_to='wc/')

    data_criacao     = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now=True)

    class Meta:
        verbose_name        = "Texto Processado"
        verbose_name_plural = "Textos Processados"
        ordering = ('data_criacao',)

    def __str__(self):
        print(self.trechos.first())
        print(self.trechos.first().text)
        # trecho = self.trechos.first().text
        # trechos = self.trechos.values_list('text', flat=True)
        # for trecho in trechos:
            # print('#  ', trecho)

        # texto_completo = ' '.join(list(self.trechos.all()))
        return self.trechos.first().text[:200]

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

