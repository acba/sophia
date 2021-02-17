from django.shortcuts import render

from apps.sophia.forms import BuscaForm
from apps.docs.models import TextDocument
from apps.audios.models import AudioDocument

##
## ROTAS LIBERADAS
##

def cover(request):
    return render(request, 'pages/cover.html')

def sobre(request):
    return render(request, 'pages/sobre.html')


##
## ROTAS PROTEGIDAS
##

def home(request):
    return render(request, 'pages/home.html')

def buscar(request):
    if request.method == 'POST':
        form = BuscaForm(request.POST)
        if form.is_valid():
            termo = request.POST['termo']

            docs = TextDocument.objects.filter(user__id=request.user.id, processedtext__texto__contains=termo).all()
            audios = AudioDocument.objects.filter(user__id=request.user.id, processedaudio__trechos__text__contains=termo).all()

        return render(request, 'pages/buscar.html', { 'resultado': True, 'docs': docs, 'audios': audios })
    else:
        form = BuscaForm()
        return render(request, 'pages/buscar.html', { 'form': form })
