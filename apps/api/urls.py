from django.conf.urls import url, include
from django.urls import path, include

from . import views

app_name= 'api'
urlpatterns = [
    path('', views.root, name='root'),
]
