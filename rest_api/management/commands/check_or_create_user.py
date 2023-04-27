import logging
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """If in development mode, check if superuser exists and create if not"""
    def handle(self, *args, **options):
        if not settings.DEBUG:
            return

        logger.info("Development mode detected, checking if superuser exists...")
        from django.contrib.auth import get_user_model

        username = os.environ.get("SUPERUSER_USERNAME")
        email = os.environ.get("SUPERUSER_EMAIL")
        password = os.environ.get("SUPERUSER_PASSWORD")

        User = get_user_model()

        try:
            if not User.objects.filter(username=username).exists():
                logger.warning("Superuser does not exist, creating...")
                User.objects.create_superuser(
                    username=username, password=password, email=email
                )
                logger.info("Superuser created")
            else:
                logger.warning("Superuser already exists")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
        except IntegrityError as e:
            logger.error(f"Integrity error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
