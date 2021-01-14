from django import forms
from .models import TextDocument

class TextDocumentForm(forms.ModelForm):
    class Meta:
        model = TextDocument
        fields = ('nome', 'file', )
