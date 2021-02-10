from django.conf.urls import url, include
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name= 'api'
urlpatterns = [
    path('', views.root, name='root'),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]
