import random
import string

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def generate_short_code() -> str:
    """Generates a random string with the given length."""
    characters = string.ascii_letters + string.digits
    return "".join(
        random.choice(characters) for _ in range(settings.SHORTENED_URL_LENGTH)
    )


def is_valid_url(url: str) -> bool:
    """Checks if the given URL is valid."""
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False
