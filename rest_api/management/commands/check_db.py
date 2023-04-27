import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Django command to check database connection"

    def handle(self, *args, **options):
        logger.info("Connecting to database...")
        is_db_available = False
        num_tries = 0
        max_tries = settings.MAX_TRIES
        seconds_to_wait = settings.SECONDS_TO_WAIT
        while not is_db_available and num_tries < max_tries:
            try:
                connection.ensure_connection()
                is_db_available = True
            except OperationalError:
                logger.warning(
                    f"Database unavailable, waiting {seconds_to_wait} seconds to try again..."
                )
                time.sleep(seconds_to_wait)
                num_tries += 1

        if is_db_available:
            logger.info("Database available, and connection is established!")
        else:
            logger.critical(
                f"After {max_tries} tries, database is still unavailable."
                f"Please check your database connection settings or database host."
                f"Aborting..."
            )
