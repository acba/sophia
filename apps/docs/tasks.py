from django.contrib.auth import get_user_model
from celery.utils.log import get_task_logger
import time

from config import celery_app

logger = get_task_logger(__name__)
User = get_user_model()

@celery_app.task(name='get_users_count_task')
def get_users_count_task():
    '''A pointless Celery task to demonstrate usage.'''
    logger.info('###### LOG Contando usuarios...')

    time.sleep(3)

    logger.info(f'###### LOG Pronto {User.objects.count()}')

    return User.objects.count()
