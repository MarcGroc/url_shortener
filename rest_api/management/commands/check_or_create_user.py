import os
import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create super user if not exists'

    def handle(self, *args, **options):
        logger.info('Check if superuser exists')
        from django.contrib.auth import get_user_model

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        User = get_user_model()

        try:
            if not User.objects.filter(username='admin').exists():
                logger.warning('Superuser does not exist, creating...')
                User.objects.create_superuser(username=username, password=password, email=email)
                logger.info('Superuser created')
            else:
                logger.warning('Superuser already exists')
        except Exception as e:
            logger.error(e)
