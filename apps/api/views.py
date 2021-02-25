from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

User = get_user_model()

from apps.api.serializers import DocSerializer, GroupSerializer, UserSerializer
from apps.docs.models import TextDocument
from apps.docs.forms import TextDocumentForm

def root(request):
    return JsonResponse({"projeto": 'Sophia' })


# class UserViewSet(viewsets.ModelViewSet):
#     """
#         API endpoint that allows users to be viewed or edited.
#     """

#     # queryset = User.objects.all().order_by('-date_joined')
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class DocViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited.
    """
    queryset = TextDocument.objects.all()
    serializer_class = DocSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FileUploadParser]


    @action(detail=True, methods=['get'])
    def status(self, request, *args, **kwargs):
        doc = self.get_object()

        return Response({
            'processando': doc.processando,
            'processado': doc.foi_processado,
        })

    def create(self, request):
        print('request.data:', request.data)
        print('request.user:', request.user)

        textdoc = TextDocument.objects.create(user=request.user, file=request.data['file'])

        # textdoc.user     = request.user
        textdoc.size     = textdoc.file.size
        textdoc.filename = textdoc.file.name
        textdoc.mime     = request.FILES['file'].content_type
        textdoc.ext      = textdoc.file.name.split('.')[-1]

        print('textdoc', textdoc)
        # textdoc.save()

        return Response({'aleatorio': 'demais'})


