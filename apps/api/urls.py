from django.conf.urls import url, include
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'docs', views.DocViewSet, basename='docs')
router.register(r'audios', views.AudioDocViewSet, basename='audios')

app_name= 'api'
urlpatterns = [
    path('', views.root, name='root'),
    path('rf/', include(router.urls)),

    # DRF auth token
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth-token/', obtain_auth_token),
]
