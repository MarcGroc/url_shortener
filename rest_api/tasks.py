from __future__ import absolute_import, unicode_literals

from datetime import timedelta
from typing import Dict, Optional, Union

from celery import shared_task
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
) -> Union[Dict[str, str], int]:
    if custom_short_code:
        try:
            ShortenedLink.objects.get(short_code=custom_short_code)
            return {"error": "Short code already exists, please try another one."}
        except ShortenedLink.DoesNotExist:
            pass

    short_url, created = ShortenedLink.objects.get_or_create(original_url=original_url)
    if created:
        short_url.short_code = (
            custom_short_code if custom_short_code else generate_short_code()
        )
        short_url.user_ip = user_ip
        short_url.user_agent = user_agent
        short_url.save()
    return short_url.id
