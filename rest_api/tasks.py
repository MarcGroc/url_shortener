from __future__ import absolute_import, unicode_literals

from datetime import timedelta
from typing import Dict, Optional

from celery import shared_task
from django.db import IntegrityError
from django.utils import timezone

from rest_api.models import ShortenedLink
from rest_api.utils import generate_short_code


@shared_task
def delete_old_urls() -> None:
    expiration_date = timezone.now() - timedelta(days=30)
    ShortenedLink.objects.filter(created_at__lt=expiration_date).delete()


@shared_task
def create_shortened_url(
    original_url: str, user_ip: str, user_agent: str, custom_short_code: Optional[str]
) -> Dict[str, str] | dict[str, int]:
    try:
        short_url = ShortenedLink.objects.get(original_url=original_url)
    except ShortenedLink.DoesNotExist:
        short_url = ShortenedLink(original_url=original_url)
        short_url.short_code = (
            custom_short_code if custom_short_code else generate_short_code()
        )
        short_url.user_ip = user_ip
        short_url.user_agent = user_agent
        try:
            short_url.save()
        except IntegrityError:
            return {"error": "Short code already exists, please try another one."}
    return {"id": short_url.id}
