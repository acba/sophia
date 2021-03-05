from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.utils import IntegrityError

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser

User = get_user_model()

from apps.utils import hash_file
from apps.api.permissions import UserIDPermission, WhiteListPermission
from apps.api.serializers import AudioDocSerializer, DocSerializer

from apps.docs.models import TextDocument
from apps.docs.tasks import processa_textdoc_task

from apps.audios.models import AudioDocument
from apps.audios.tasks import processa_audiodoc_task


def root(request):
    return JsonResponse({"projeto": 'Sophia' })

class DocViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited.
    """
    queryset = TextDocument.objects.all()
    serializer_class = DocSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & WhiteListPermission
        & UserIDPermission
    ]
    # parser_classes = [FileUploadParser]
    parser_classes = [MultiPartParser]

    @action(detail=True, methods=['get'])
    def status(self, request, *args, **kwargs):
        doc = self.get_object()

        return Response({
            'processando': doc.processando,
            'processado': doc.foi_processado,
        })

    def create(self, request):
        data = dict(request.data)

        if 'files' not in data:
            return Response({
                'status': False,
                'msg': 'Nenhum documento anexado encontrado'
            })

        resultado = []
        anexos = data['files']
        for anexo in anexos:

            if not anexo.content_type.startswith('audio') \
                and not anexo.content_type.startswith('video'):

                api_userid = request.META.get('HTTP_X_API_USERID', None)
                hash_sha256 = hash_file(anexo)

                try:
                    textdoc = TextDocument.objects.create(user=request.user, api_user=api_userid, hashfile=hash_sha256, file=anexo)

                    textdoc.nome     = anexo.name
                    textdoc.size     = anexo.size
                    textdoc.filename = anexo.name
                    textdoc.mime     = anexo.content_type
                    textdoc.ext      = textdoc.file.name.split('.')[-1]
                    # textdoc.save()

                    resultado.append({
                        'filename': anexo.name,
                        'msg': 'Documento criado com sucesso'
                    })
                except IntegrityError:
                    resultado.append({
                        'filename': anexo.name,
                        'msg': 'Documento já existente para o usuário'
                    })
            else:
                resultado.append({
                    'filename': anexo.name,
                    'msg': 'Rota não funciona para audios ou videos, favor consultar rota /audios'
                })

        return Response({
            'status': True,
            'msg': 'Consulta processada com sucesso',
            'data': resultado
        })


    @action(detail=True, methods=['post'])
    def processa(self, request, *args, **kwargs):

        docid = kwargs['pk']
        textdoc = TextDocument.objects.filter(user__id=request.user.id, id=docid).first()

        if textdoc is None:
            return Response({ 'status': False, 'msg': 'Doc não encontrado' })

        if textdoc.foi_processado:
            return Response({ 'status': False, 'msg': 'Doc já processado', 'data': textdoc.id })

        if textdoc.processando:
            return Response({ 'status': False, 'msg': 'Doc está sendo processado', 'data': textdoc.id })

        textdoc.processando = True
        textdoc.save()

        processa_task = processa_textdoc_task.delay(userid=request.user.id, docid=docid)

        return Response({
            'status': True,
            'msg': 'Doc está sendo processado'

        })

class AudioDocViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited.
    """
    queryset = AudioDocument.objects.all()
    serializer_class = AudioDocSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & WhiteListPermission
        & UserIDPermission
    ]
    parser_classes = [FileUploadParser]

    @action(detail=True, methods=['get'])
    def status(self, request, *args, **kwargs):
        doc = self.get_object()

        return Response({
            'processando': doc.processando,
            'processado': doc.foi_processado,
        })

    def create(self, request):

        if 'file' not in request.data:
            return Response({
                'status': False,
                'msg': 'Documento anexado não encontrado'
            })

        if not request.data['file'].content_type.startswith('audio') and \
            not request.data['file'].content_type.startswith('video'):
            return Response({
                'status': False,
                'msg': 'Rota funciona apenas para audios ou videos, favor consultar outra rota.'
            })

        api_userid = request.META.get('HTTP_X_API_USERID', None)
        hash_sha256 = hash_file(request.data['file'])

        try:
            audiodoc = AudioDocument.objects.create(user=request.user, api_user=api_userid, hashfile=hash_sha256, file=request.data['file'])
        except IntegrityError:
            return Response({
                'status': False,
                'msg': 'Audio já existente para o usuário'
            })

        audiodoc.nome     = request.data['file'].name
        audiodoc.size     = audiodoc.file.size
        audiodoc.filename = request.data['file'].name
        audiodoc.mime     = request.FILES['file'].content_type
        audiodoc.ext      = audiodoc.file.name.split('.')[-1]
        audiodoc.save()

        return Response({
            'status': True,
            'msg': 'Audio criado com sucesso',
            'data': audiodoc.id,
        })

    @action(detail=True, methods=['post'])
    def processa(self, request, *args, **kwargs):

        docid = kwargs['pk']
        audiodoc = AudioDocument.objects.filter(user__id=request.user.id, id=docid).first()

        if audiodoc is None:
            return Response({ 'status': False, 'msg': 'Audio não encontrado' })

        if audiodoc.foi_processado:
            return Response({ 'status': False, 'msg': 'Audio já processado', 'data': audiodoc.id })

        if audiodoc.processando:
            return Response({ 'status': False, 'msg': 'Audio está sendo processado', 'data': audiodoc.id })

        audiodoc.processando = True
        audiodoc.save()

        processa_task = processa_audiodoc_task.delay(userid=request.user.id, docid=docid)

        return Response({
            'status': True,
            'msg': 'Audio está sendo processado'
        })


