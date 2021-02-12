from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from apps.docs.forms import TextDocumentForm
from apps.docs.models import TextDocument
from apps.docs.tables import TextDocumentTable
from apps.docs.tasks import  processa_textdoc_task

@login_required(login_url=reverse_lazy('account_login'))
def lista_docs(request):
    meus_docs = TextDocument.objects.filter(user__id=request.user.id)
    table = TextDocumentTable(meus_docs)
    table.paginate(page=request.GET.get('page', 1), per_page=5)

    return render(request, 'docs.html', { 'meus_docs': meus_docs, 'table': table })

@login_required(login_url=reverse_lazy('account_login'))
def detalhe_doc(request, docid):
    textdoc = TextDocument.objects.filter(user__id=request.user.id, id=docid).first()

    return render(request, 'docs_detalhe.html', { 'textdoc': textdoc })

@login_required(login_url=reverse_lazy('account_login'))
def remove_doc(request):
    if request.method == 'POST' and 'id' in request.POST:
        docid = request.POST['id']
        TextDocument.objects.filter(user__id=request.user.id, id=docid).delete()
        return HttpResponseRedirect(reverse('docs:lista_docs'))
    elif request.method == 'GET' and 'id' in request.GET:
        docid = request.GET['id']
        TextDocument.objects.filter(user__id=request.user.id, id=docid).delete()
        return HttpResponseRedirect(reverse('docs:lista_docs'))
    else:
        return HttpResponseRedirect(reverse('docs:lista_docs'))

@login_required(login_url=reverse_lazy('account_login'))
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

@login_required(login_url=reverse_lazy('account_login'))
def processa_doc(request, docid):
    if request.method == 'GET':
        textdoc = TextDocument.objects.filter(user__id=request.user.id, id=docid).first()
        textdoc.processando = True
        textdoc.save()

        processa_task = processa_textdoc_task.delay(userid=request.user.id, docid=docid)
        task_id = processa_task.task_id

        return render(request, 'docs_detalhe.html', { 'textdoc': textdoc, 'task_id': task_id })
    else:
        form = TextDocumentForm()

    return render(request, 'docs.html', { 'form': form })
