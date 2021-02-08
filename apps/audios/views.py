from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files import File

from .forms import AudioDocumentForm
from .tables import AudioDocumentTable
from .models import AudioDocument, ProcessedAudio, TermoFreqData, LegendaTrecho

from apps.utils import silent_remove
from apps.utils.wordcloud import WordCloudProcessor
from apps.utils.textprocessor import TextProcessor
from apps.utils.recognizer import vr, gr

def lista_audios(request):
    meus_audios = AudioDocument.objects.filter(user__id=request.user.id)
    table = AudioDocumentTable(meus_audios)
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    return render(request, 'audios.html', { 'meus_audios': meus_audios, 'table': table })

def detalhe_audio(request, audioid):
    audiodoc = AudioDocument.objects.filter(user__id=request.user.id, id=audioid).first()
    return render(request, 'audio_detalhe.html', { 'audiodoc': audiodoc })

def remove_audio(request):
    if request.method == 'POST' and 'id' in request.POST:
        audioid = request.POST['id']
        AudioDocument.objects.filter(user__id=request.user.id, id=audioid).delete()
        return HttpResponseRedirect(reverse('audios:lista_audios'))
    elif request.method == 'GET' and 'id' in request.GET:
        audioid = request.GET['id']
        AudioDocument.objects.filter(user__id=request.user.id, id=audioid).delete()
        return HttpResponseRedirect(reverse('audios:lista_audios'))
    else:
        return HttpResponseRedirect(reverse('audios:lista_audios'))

def upload_audio(request):
    if request.method == 'POST':
        form = AudioDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            audiodoc = form.save(commit=False)

            audiodoc.user     = request.user
            audiodoc.size     = audiodoc.file.size
            audiodoc.filename = audiodoc.file.name
            audiodoc.mime     = request.FILES['file'].content_type
            audiodoc.ext      = audiodoc.file.name.split('.')[-1]

            audiodoc.save()
            return HttpResponseRedirect(reverse('audios:lista_audios'))
    else:
        form = AudioDocumentForm()

    return render(request, 'audio_upload.html', { 'form': form })

def processa_audio(request, audioid, processor):
    if request.method == 'GET':
        audiodoc = AudioDocument.objects.filter(id=audioid).first()

        if processor == 'vr':
            proc = 'Vosk'
            lista_vtt = vr.file_to_vtt(audiodoc.file.path)
        elif processor == 'gr':
            proc = 'Google'
            lista_vtt = gr.file_to_vtt(audiodoc.file.path)
        # Default é o VOSK
        else:
            proc = 'Vosk'
            lista_vtt = vr.file_to_vtt(audiodoc.file.path)

        texto = ''
        for t in lista_vtt:
            texto += t['text'] + ' '
        texto = texto.strip()

        tp = TextProcessor(texto)
        tp.clean()
        info = tp.info()

        # Cria ProcessedAudio
        pa = ProcessedAudio.objects.create(audiodoc=audiodoc, processor=proc)

        # Cria o arquivo Wordcloud
        wp = WordCloudProcessor(tp.remove_stopwords())
        wp.generate_wordcloud()
        wp.wc2png(audiodoc.file.path)
        django_file = File(open(f'{audiodoc.file.path}.wordcloud.png','rb'))
        pa.file_wc.save(f'{audiodoc.filename}.wordcloud.png', django_file)
        pa.save()

        # Exclui arquito temporario criado
        silent_remove(f'{audiodoc.file.path}.wordcloud.png')

        # Cria Trechos de Legenda
        for trecho in lista_vtt:
            l = LegendaTrecho(start=trecho['start'], text=trecho['text'], pdoc=pa)
            l.save()

        # Cria Informacoes de dados mais frequentes
        for dado in info['mais_frequentes']:
            c = TermoFreqData.objects.create(termo=dado[0], qtd=dado[1], pdoc=pa)
            c.save()

        audiodoc.foi_processado = True
        audiodoc.save()

        return HttpResponseRedirect(reverse('audios:audio', args=[audioid]))
    else:
        form = AudioDocumentForm()

    return render(request, 'audios.html', { 'form': form })
