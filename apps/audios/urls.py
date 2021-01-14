from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'audios'
urlpatterns = [
    path('', views.lista_audios, name='lista_audios'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('<int:audioid>/', views.detalhe_audio, name='audio'),
    path('<int:audioid>/transcreve/', views.transcreve_audio, name='transcreve_audio'),
]
