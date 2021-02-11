from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from apps.audios.forms import AudioDocumentForm
from apps.audios.tables import AudioDocumentTable
from apps.audios.models import AudioDocument
from apps.audios.tasks import processa_audiodoc_task

@login_required(login_url=reverse_lazy('account_login'))
def lista_audios(request):
    meus_audios = AudioDocument.objects.filter(user__id=request.user.id)
    table = AudioDocumentTable(meus_audios)
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    return render(request, 'audios.html', { 'meus_audios': meus_audios, 'table': table })

@login_required(login_url=reverse_lazy('account_login'))
def detalhe_audio(request, audioid):
    audiodoc = AudioDocument.objects.filter(user__id=request.user.id, id=audioid).first()
    return render(request, 'audio_detalhe.html', { 'audiodoc': audiodoc })

@login_required(login_url=reverse_lazy('account_login'))
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

@login_required(login_url=reverse_lazy('account_login'))
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

@login_required(login_url=reverse_lazy('account_login'))
def processa_audio(request, audioid, processor):
    if request.method == 'GET':
        audiodoc = AudioDocument.objects.filter(user__id=request.user.id, id=audioid).first()
        audiodoc.processando = True
        audiodoc.save()

        processa_task = processa_audiodoc_task.delay(userid=request.user.id, audioid=audioid, processor=processor)
        task_id = processa_task.task_id

        return render(request, 'audio_detalhe.html', { 'audiodoc': audiodoc, 'task_id': task_id })
    else:
        form = AudioDocumentForm()

    return render(request, 'audios.html', { 'form': form })
