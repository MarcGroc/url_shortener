from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import ShortenedLink
from .utils import generate_short_code


@shared_task
def delete_old_urls() -> None:
    expiration_date = timezone.now() - timedelta(days=30)
    ShortenedLink.objects.filter(created_at__lt=expiration_date).delete()


@shared_task(bind=True)
def create_shortened_url(self, original_url, user_ip, user_agent) -> int:
    short_url, created = ShortenedLink.objects.get_or_create(original_url=original_url)
    if created:
        short_url.short_code = generate_short_code()
        short_url.user_ip = user_ip
        short_url.user_agent = user_agent
        short_url.save()
    return short_url.id
