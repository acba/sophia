from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'audios'
urlpatterns = [
    path('', views.lista_audios, name='lista_audios'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('remove/', views.remove_audio, name='remove_audio'),
    path('<int:audioid>/', views.detalhe_audio, name='audio'),
    path('<int:audioid>/processa/<str:processor>', views.processa_audio, name='processa_audio'),
]
