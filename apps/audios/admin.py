from django.contrib import admin

# Register your models here.

from .forms import AudioDocumentForm
from .models import AudioDocument

# Register your models here.

@admin.register(AudioDocument)
class DocumentAdmin(admin.ModelAdmin):
    form = AudioDocumentForm
