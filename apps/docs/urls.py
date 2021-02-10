from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'docs'
urlpatterns = [
    path('', views.lista_docs, name='lista_docs'),
    path('upload/', views.upload_doc, name='upload_doc'),
    path('remove/', views.remove_doc, name='remove_doc'),
    path('<int:docid>/', views.detalhe_doc, name='doc'),
    path('<int:docid>/processa/', views.processa_doc, name='processa_doc'),
]
