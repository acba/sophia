from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TextDocumentForm
from .models import TextDocument

from apps.utils.textprocessor import tp_factory
from apps.utils.wordcloud import WordCloudProcessor


def lista_docs(request):
    if request.method == 'POST':
        form = TextDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        form = TextDocumentForm()
        meus_docs = TextDocument.objects.all()

        return render(request, 'docs.html', { 'form': form, 'meus_docs': meus_docs })

def upload_doc(request):
    if request.method == 'POST':
        form = TextDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            f = form.save(commit=False)

            f.size     = f.file.size
            f.filename = f.file.name
            f.mime     = request.FILES['file'].content_type
            f.ext      = f.file.name.split('.')[-1]

            f.save()

            return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        form = TextDocumentForm()

    return render(request, 'docs_upload.html', { 'form': form })

def detalhe_doc(request, docid):
    textdoc = TextDocument.objects.filter(id=docid).first()
    return render(request, 'docs_detalhe.html', { 'textdoc': textdoc })

def transcreve_doc(request, docid):
    if request.method == 'GET':
        textdoc = TextDocument.objects.filter(id=docid).first()

        tp = tp_factory(textdoc.file)
        texto = tp.extract()
        texto = tp.clean()

        textdoc.transcricao = texto
        textdoc.foi_transcrito = True

        textdoc.save()

        return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        form = TextDocumentForm()

    return render(request, 'docs.html', { 'form': form })

def processa_doc(request, docid):
    if request.method == 'GET':
        textdoc = TextDocument.objects.filter(id=docid).first()

        tp = tp_factory(textdoc.transcricao)
        info = tp.info()
        print(info)

        texto_sem_stopwords = tp.remove_stopwords()
        wp = WordCloudProcessor(texto_sem_stopwords)
        wp.generate_wordcloud()
        wp.wc2png(textdoc.file.path)

        return render(request, 'docs_detalhe.html', { 'textdoc': textdoc, 'info': info })
    else:
        form = TextDocumentForm()

    return render(request, 'docs.html', { 'form': form })
