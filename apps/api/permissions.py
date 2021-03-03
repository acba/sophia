from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from netaddr import IPAddress

REST_SAFE_LIST_IPS = [
    '127.0.0.1',
    '10.128.24.',   # example IP
    '192.168.0.',     # the local subnet, stop typing when subnet is filled out
]


class IPNotAllowed(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'IP não permitido'}
    default_code = 'not_allowed'


class WhiteListPermission(BasePermission):
    """
        Libera apenas requisição para a API de IPs internos.
    """

    def has_permission(self, request, view):
        remote_addr = request.META['REMOTE_ADDR']
        ip = IPAddress(remote_addr)

        if ip.is_private():
            return True
        else:
            raise IPNotAllowed()


class UserIDNotFound(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'Header X_API_USERID não encontrado'}
    default_code = 'not_found'


class UserIDPermission(BasePermission):
    """
        Libera apenas requisição para a API de IPs internos.
    """

    def has_permission(self, request, view):
        api_userid = request.META.get('HTTP_X_API_USERID', None)

        if api_userid is not None:
            return True
        else:
            raise UserIDNotFound()
