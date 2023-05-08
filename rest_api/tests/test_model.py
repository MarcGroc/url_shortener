from django.test import TestCase

from rest_api.models import ShortenedLink


class ShortenedLinkModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.shortened_link = {
            "original_url": "https://www.google.com",
            "short_code": "hiwhdhh12",
            "created_at": "2023-04-01 12:00:00",
            "visits": 0,
            "user_ip": "0.0.0.0",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        }

    def test_shortened_link_model_data_should_be_valid(self):
        self.assertEqual(self.shortened_link["original_url"], "https://www.google.com")
        self.assertEqual(self.shortened_link["short_code"], "hiwhdhh12")
        self.assertEqual(self.shortened_link["created_at"], "2023-04-01 12:00:00")
        self.assertEqual(self.shortened_link["visits"], 0)
        self.assertEqual(self.shortened_link["user_ip"], "0.0.0.0")
        self.assertEqual(
            self.shortened_link["user_agent"],
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        )
        shortened_link = ShortenedLink.objects.create(
            original_url=self.shortened_link["original_url"],
            short_code=self.shortened_link["short_code"],
        )

        self.assertEqual(
            shortened_link.original_url, self.shortened_link["original_url"]
        )
        self.assertEqual(shortened_link.short_code, self.shortened_link["short_code"])
