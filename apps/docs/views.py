from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files import File

from .forms import TextDocumentForm
from .models import TextDocument, ProcessedText, CPFData, CNPJData, EmailData, URLData, TelefoneData, TermoFreqData

from apps.utils.textprocessor import tp_factory
from apps.utils.wordcloud import WordCloudProcessor
from apps.utils import silent_remove
from apps.docs.tables import TextDocumentTable



def lista_docs(request):
    meus_docs = TextDocument.objects.filter(user__id=request.user.id)
    table = TextDocumentTable(meus_docs)
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    return render(request, 'docs.html', { 'meus_docs': meus_docs, 'table': table })

def detalhe_doc(request, docid):
    textdoc = TextDocument.objects.filter(id=docid).first()
    return render(request, 'docs_detalhe.html', { 'textdoc': textdoc })

def remove_doc(request, docid):
    TextDocument.objects.filter(id=docid).delete()
    return HttpResponseRedirect(reverse('docs:lista_docs'))

def upload_doc(request):
    if request.method == 'POST':
        form = TextDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            textdoc = form.save(commit=False)

            textdoc.user     = request.user
            textdoc.size     = textdoc.file.size
            textdoc.filename = textdoc.file.name
            textdoc.mime     = request.FILES['file'].content_type
            textdoc.ext      = textdoc.file.name.split('.')[-1]

            textdoc.save()

            return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        form = TextDocumentForm()

    return render(request, 'docs_upload.html', { 'form': form })

def processa_doc(request, docid):
    if request.method == 'GET':
        textdoc = TextDocument.objects.filter(id=docid).first()

        tp = tp_factory(textdoc.file, textdoc.mime)
        texto = tp.extract()
        texto = tp.clean()
        info  = tp.info()

        # Cria ProcessedText
        pt = ProcessedText.objects.create(texto=texto, textdoc=textdoc)

        # Cria o arquivo WordCloud
        wp = WordCloudProcessor(tp.remove_stopwords())
        wp.generate_wordcloud()
        wp.wc2png(textdoc.file.path)
        django_file = File(open(f'{textdoc.file.path}.wordcloud.png','rb'))
        pt.file_wc.save(f'{textdoc.filename}.wordcloud.png', django_file)
        pt.save()

        # Exclui arquito temporario criado
        silent_remove(f'{textdoc.file.path}.wordcloud.png')

        # Salva os dados encontrados no texto processado
        for cpf in info['cpfs']:
            c = CPFData.objects.create(cpf=cpf, pdoc=pt)
            c.save()

        for cnpj in info['cnpjs']:
            c = CNPJData.objects.create(cnpj=cnpj, pdoc=pt)
            c.save()

        for email in info['emails']:
            c = EmailData.objects.create(email=email, pdoc=pt)
            c.save()

        for url in info['urls']:
            c = URLData.objects.create(url=url, pdoc=pt)
            c.save()

        for telefone in info['telefones']:
            c = TelefoneData.objects.create(telefone=telefone, pdoc=pt)
            c.save()

        # Cria Informacoes de dados mais frequentes
        for dado in info['mais_frequentes']:
            c = TermoFreqData.objects.create(termo=dado[0], qtd=dado[1], pdoc=pt)
            c.save()

        textdoc.foi_processado = True
        textdoc.save()

        return HttpResponseRedirect(reverse('docs:doc', args=[docid]))
    else:
        form = TextDocumentForm()

    return render(request, 'docs.html', { 'form': form })
