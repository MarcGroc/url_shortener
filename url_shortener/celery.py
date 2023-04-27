from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_shortener.settings")
app = Celery("url_shortener")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
     'delete_old_urls': {
        'task': 'app.tasks.delete_old_urls',
        'schedule': timedelta(days=1),
    },
}