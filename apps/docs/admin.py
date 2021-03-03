from django.contrib import admin

from .models import TextDocument, ProcessedText
from .forms import TextDocumentForm

@admin.register(TextDocument)
class DocumentAdmin(admin.ModelAdmin):
    form = TextDocumentForm
    list_display = ('nome', 'file', 'user', 'filename', 'size', 'mime', 'ext', 'data_upload', 'data_atualizacao')
    fields = ('nome', 'file', 'user', 'api_user', 'filename', 'hashfile', 'size', 'mime', 'ext', 'foi_processado', 'processando')


@admin.register(ProcessedText)
class ProcessedDocumentAdmin(admin.ModelAdmin):
    list_display = ('nomedoc', 'preview', 'file_wc', 'data_criacao', 'data_atualizacao')

    def nomedoc(self, obj):
        return obj.textdoc.nome

    def preview(self, obj):
        return obj.texto[:200]
