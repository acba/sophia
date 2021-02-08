from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'docs/user_{0}/{1}'.format(instance.user.id, filename)

class TextDocument(models.Model):
    """
        Classe que representa o objeto TextDocument
    """

    nome = models.CharField('Descrição do Documento', max_length=255, blank=True)
    file = models.FileField('Arquivo', upload_to=user_directory_path)
    user = models.ForeignKey('users.User', related_name="textdocs", on_delete=models.CASCADE, null=False, default=None)

    filename = models.CharField('Nome do Arquivo', max_length=255, blank=True)
    size     = models.BigIntegerField('Tamanho Arquivo', null=True)
    mime     = models.CharField('MIME Type', max_length=255, blank=True)
    ext      = models.CharField('Extensão', max_length=255, blank=True)

    data_upload      = models.DateTimeField('Data de Upload', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now=True)

    foi_processado = models.BooleanField('Foi Processado', default=False)
    class Meta:
        verbose_name        = "Documento de Texto"
        verbose_name_plural = "Documentos de Texto"
        ordering = ('data_upload',)

    def __str__(self):
        return self.nome[:50] + self.filename


class ProcessedText(models.Model):
    textdoc = models.OneToOneField(TextDocument, related_name='processedtext', on_delete=models.CASCADE, primary_key=True)
    texto   = models.TextField('Texto Transcrito', default=None, null=True)

    file_wc = models.FileField('Wordcloud', upload_to='wc/')

    data_criacao     = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização',auto_now=True)

    class Meta:
        verbose_name        = "Texto Processado"
        verbose_name_plural = "Textos Processados"
        ordering = ('data_criacao',)

    def __str__(self):
        return self.texto[:200]

class CPFData(models.Model):
    cpf = models.CharField('CPF', max_length=255, blank=True)
    pdoc = models.ForeignKey(ProcessedText, related_name="cpfs", on_delete=models.CASCADE, null=False, default=None)

class CNPJData(models.Model):
    cnpj = models.CharField('CNPJ', max_length=255, blank=True)
    pdoc = models.ForeignKey(ProcessedText, related_name="cnpjs", on_delete=models.CASCADE, null=False, default=None)

class EmailData(models.Model):
    email = models.CharField('E-Mail', max_length=255, blank=True)
    pdoc = models.ForeignKey(ProcessedText, related_name="emails", on_delete=models.CASCADE, null=False, default=None)

class TelefoneData(models.Model):
    telefone = models.CharField('Telefone', max_length=255, blank=True)
    pdoc = models.ForeignKey(ProcessedText, related_name="telefones", on_delete=models.CASCADE, null=False, default=None)

class URLData(models.Model):
    url = models.CharField('URL', max_length=255, blank=True)
    pdoc = models.ForeignKey(ProcessedText, related_name="urls", on_delete=models.CASCADE, null=False, default=None)

class TermoFreqData(models.Model):
    termo = models.CharField('Termo', max_length=255, blank=True)
    qtd   = models.IntegerField('Qtd', blank=True)

    pdoc = models.ForeignKey(ProcessedText, related_name="mais_frequentes", on_delete=models.CASCADE, null=False, default=None)


# Whenever ANY model is deleted, if it has a file field on it, delete the associated file too
@receiver(post_delete, sender=TextDocument)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

# Whenever ANY model is deleted, if it has a file field on it, delete the associated file too
@receiver(post_delete, sender=ProcessedText)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)

# Only delete the file if no other instances of that model are using it
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)
