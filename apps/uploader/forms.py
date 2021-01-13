from django import forms
from .models import AudioDocument, TextDocument

class AudioDocumentForm(forms.ModelForm):
    class Meta:
        model = AudioDocument
        fields = ('description', 'document', )

class TextDocumentForm(forms.ModelForm):
    class Meta:
        model = TextDocument
        fields = ('description', 'document', )
