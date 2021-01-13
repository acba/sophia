from django.contrib import admin

from .forms import AudioDocumentForm
from .models import AudioDocument

# Register your models here.

@admin.register(AudioDocument)
class DocumentAdmin(admin.ModelAdmin):
    form = AudioDocumentForm
