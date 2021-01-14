from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AudioDocumentForm
from .models import AudioDocument

from apps.utils.recognizer import vr

def lista_audios(request):
    if request.method == 'POST':
        form = AudioDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('audios:lista_audios'))
    else:
        form = AudioDocumentForm()
        meus_audios = AudioDocument.objects.all()

        return render(request, 'audios.html', { 'form': form, 'meus_audios': meus_audios })

def detalhe_audio(request, audioid):
    audiodoc = AudioDocument.objects.filter(id=audioid).first()
    return render(request, 'audio_detalhe.html', { 'audiodoc': audiodoc })

def upload_audio(request):
    if request.method == 'POST':
        form = AudioDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('audios:lista_audios'))
    else:
        form = AudioDocumentForm()

    return render(request, 'audio_upload.html', { 'form': form })

def transcreve_audio(request, audioid):
    if request.method == 'GET':
        audiodoc = AudioDocument.objects.filter(id=audioid).first()

        stream = vr.read_file(audiodoc.doc.path)
        dados = vr.stream_to_text(stream)

        audiodoc.transcricao = dados
        audiodoc.foi_transcrito = True
        audiodoc.save()

        return HttpResponseRedirect(reverse('audios:lista_audios'))
    else:
        form = AudioDocumentForm()

    return render(request, 'audios.html', { 'form': form })
