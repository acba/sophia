from django.contrib import admin

from .models import TextDocument
from .forms import TextDocumentForm

@admin.register(TextDocument)
class DocumentAdmin(admin.ModelAdmin):
    form = TextDocumentForm
