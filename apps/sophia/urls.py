from django.urls import path

from . import views

app_name= 'sophia'
urlpatterns = [
    path('', views.cover, name='cover'),
    path('home/', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('sobre/', views.sobre, name='sobre'),
]
