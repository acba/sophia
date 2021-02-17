from django import forms

class BuscaForm(forms.Form):
    termo = forms.CharField(max_length=100)
