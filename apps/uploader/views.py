from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AudioDocumentForm, TextDocumentForm

def model_form_upload(request):
    if request.method == 'POST':
        form = AudioDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sophia:home'))
    else:
        form = AudioDocumentForm()
    return render(request, 'model_form_upload.html', { 'form': form })
