from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TextDocumentForm
from .models import TextDocument

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


def processa_doc(request, docid):
    if request.method == 'GET':
        textdoc = TextDocument.objects.filter(id=docid).first()

        # stream = vr.read_file(audiodoc.doc.path)
        # dados = vr.stream_to_text(stream)

        # audiodoc.transcricao = dados
        # audiodoc.foi_transcrito = True
        # audiodoc.save()

        return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        form = TextDocumentForm()

    return render(request, 'docs.html', { 'form': form })
