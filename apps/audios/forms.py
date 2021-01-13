from django import forms
from .models import AudioDocument

class AudioDocumentForm(forms.ModelForm):
    class Meta:
        model = AudioDocument
        fields = ('nome', 'doc', )
