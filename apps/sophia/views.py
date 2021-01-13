from django.shortcuts import render

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
