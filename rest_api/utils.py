import random
import string
from django.conf import settings


def generate_short_code() -> str:
    """Generates a random string with the given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(settings.SHORTENED_URL_LENGTH))
