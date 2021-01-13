from .base import *
from .base import env


# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY', default='MGtdHjKHzf00WvWzMs0GdFWnucczB8wXVsb0jAVRMpYdBu2F6bK997WDwN3EQNeQ')

ALLOWED_HOSTS = [
]
