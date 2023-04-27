import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_api.models import ShortenedLink


class ShortenedURLCreateAPIViewTests(APITestCase):
    def setUp(self) -> None:
        ShortenedLink.objects.all().delete()
        self.shortened_link = {
            "original_url": "https://www.google.com",
            "short_code": "hiwhdhh12",
            "created_at": "2023-04-01 12:00:00",
            "visits": 0,
            "user_ip": "0.0.0.0",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        }

    def test_should_create_object(self):
        self.client.post(
            reverse("shortened-link-create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )
        self.assertEqual(ShortenedLink.objects.count(), 1)

    def test_should_return_400_if_url_is_not_valid(self):
        self.shortened_link["original_url"] = "not valid url"
        response = self.client.post(
            reverse("shortened-link-create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_object_if_original_url_already_in_database(self):
        ShortenedLink.objects.create(
            original_url=self.shortened_link["original_url"],
            short_code=self.shortened_link["short_code"],
        )
        self.assertEqual(ShortenedLink.objects.count(), 1)

        response = self.client.post(
            reverse("shortened-link-create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShortenedLink.objects.count(), 1)
