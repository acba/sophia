from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

def cria_superusuario(username, email):
    try:
        u = User.objects.create_superuser(username, email, 'gaeco@123')
        u.save()

    except IntegrityError:
        pass

def popula_superusuarios():
    cria_superusuario('labld', 'labld@mppb.mp.br')

    print('Superusuarios populados')

class Command(BaseCommand):
    help = 'Popula o banco'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', type=str, help='Indica o model a ser populado.')

    def handle(self, *args, **kwargs):
        _model = kwargs['model']

    popula_superusuarios()
