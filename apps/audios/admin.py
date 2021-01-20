from django.contrib import admin

# Register your models here.

from .forms import AudioDocumentForm
from .models import AudioDocument, ProcessedAudio

# Register your models here.

@admin.register(AudioDocument)
class DocumentAdmin(admin.ModelAdmin):
    form = AudioDocumentForm
    list_display = ('nome', 'file', 'user', 'filename', 'size', 'mime', 'ext', 'data_upload', 'data_atualizacao')
    fields = ('nome', 'file', 'user', 'filename', 'size', 'mime', 'ext', 'foi_processado')

@admin.register(ProcessedAudio)
class ProcessedDocumentAdmin(admin.ModelAdmin):
    list_display = ('nomedoc', 'preview', 'file_wc', 'data_criacao', 'data_atualizacao')

    def nomedoc(self, obj):
        return obj.audiodoc.nome

    def preview(self, obj):
        return obj.texto[:200]
