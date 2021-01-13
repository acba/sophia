from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'uploader'
urlpatterns = [
    path('', views.model_form_upload, name='model_form_upload'),
]
