from django.conf.urls import url, include
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='users')
router.register(r'groups', views.GroupViewSet, basename='groups')
router.register(r'docs', views.DocViewSet, basename='docs')

app_name= 'api'
urlpatterns = [
    path('', views.root, name='root'),
    path('rf/', include(router.urls)),
    # path('help', views.root, name='root'),

    # Enviar documento
    # path('upload/doc', views.root, name='root'),


    # DRF auth token
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth-token/', obtain_auth_token),
]
