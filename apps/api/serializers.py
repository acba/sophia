from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from apps.docs.models import ProcessedText, TextDocument

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProcessedDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessedText
        fields = [
            'texto', 'file_wc', 'data_criacao', 'data_atualizacao'
        ]

class DocSerializer(serializers.ModelSerializer):
    processedtext = ProcessedDocSerializer()

    class Meta:
        model = TextDocument
        fields = [
            'id', 'nome', 'filename', 'file', 'size',
            'mime', 'ext', 'data_upload', 'data_atualizacao',
            'processando', 'foi_processado', 'processedtext'
        ]

    def create(self, validated_data):
        """
            Create and return a new `TextDocument` instance, given the validated data.
        """
        return TextDocument.objects.create(**validated_data)
