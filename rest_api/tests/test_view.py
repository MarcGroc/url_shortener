import json
from unittest.mock import ANY, MagicMock, patch

from django.urls import reverse
from django_fakeredis import FakeRedis
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

    @patch("rest_api.tasks.create_shortened_url.apply_async")
    def test_should_return_201(self, mock_create_shortened_url):
        short_url = ShortenedLink.objects.create(
            original_url="https://www.example.com",
            short_code="testcode",
            user_ip="0.0.0.0",
            user_agent="Test User Agent",
        )

        mock_async_result = MagicMock()
        mock_async_result.get.return_value = short_url.id
        mock_create_shortened_url.return_value = mock_async_result

        response = self.client.post(
            reverse("create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )
        self.assertEqual(ShortenedLink.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_return_400_if_url_is_not_valid(self):
        self.shortened_link["original_url"] = "not valid url"
        response = self.client.post(
            reverse("create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("rest_api.tasks.create_shortened_url.delay")
    def test_should_return_object_if_original_url_already_in_database(
        self, mock_create_shortened_url
    ):
        shortened_link = ShortenedLink.objects.create(
            original_url=self.shortened_link["original_url"],
            short_code=self.shortened_link["short_code"],
        )
        self.assertEqual(ShortenedLink.objects.count(), 1)

        async_result_mock = MagicMock()
        async_result_mock.get.return_value = shortened_link.id
        mock_create_shortened_url.return_value = async_result_mock

        self.client.post(
            reverse("create"),
            json.dumps(self.shortened_link),
            content_type="application/json",
        )

        mock_create_shortened_url.assert_called_once_with(
            self.shortened_link["original_url"],
            ANY,
            ANY,
            ANY,
        )
        self.assertEqual(ShortenedLink.objects.count(), 1)


class RedirectToOriginalURLViewTests(APITestCase):
    def setUp(self) -> None:
        self.shortened_link = ShortenedLink.objects.create(
            original_url="https://www.google.com",
            short_code="hiwhdhh12",
            visits=0,
        )

    @FakeRedis(path="rest_api.views")
    def test_should_increment_visits_on_shortened_url(self):
        initial_visits = self.shortened_link.visits

        response = self.client.get(
            reverse("redirect", args=[self.shortened_link.short_code])
        )

        self.shortened_link.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(self.shortened_link.visits, initial_visits + 1)


class UserShortenedURLListViewTests(APITestCase):
    def setUp(self) -> None:
        # ShortenedLink.objects.all().delete()
        self.shortened_link = {
            "original_url": "https://www.google.com",
            "short_code": "hi1",
            "created_at": "2023-04-01 12:00:00",
            "visits": 0,
            "user_ip": "0.0.0.0",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        }
        self.other_user_ip = "1.1.1.1"

    @FakeRedis(path="rest_api.views")
    def test_should_return_user_shortened_url_list_based_on_user_IP(self):
        # Create two shortened URLs with the same user IP address
        ShortenedLink.objects.create(
            original_url="https://www.example.com",
            short_code="testcode1",
            user_ip=self.shortened_link["user_ip"],
        )
        ShortenedLink.objects.create(
            original_url="https://www.example2.com",
            short_code="testcode2",
            user_ip=self.shortened_link["user_ip"],
        )

        # Create a shortened URL with a different user IP address
        ShortenedLink.objects.create(
            original_url="https://www.example3.com",
            short_code="testcode3",
            user_ip=self.other_user_ip,
        )

        response = self.client.get(
            reverse("user-urls"), **{"REMOTE_ADDR": self.shortened_link["user_ip"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["user_ip"], self.shortened_link["user_ip"])
        self.assertEqual(response.data[1]["user_ip"], self.shortened_link["user_ip"])
