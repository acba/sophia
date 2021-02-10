from django.core.management.base import BaseCommand
from apps.utils.textprocessor import init_nltk

class Command(BaseCommand):
    help = 'Captura as dependencias do NLTK'

    def handle(self, *args, **kwargs):
        pass

    init_nltk()
