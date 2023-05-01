from django.urls import reverse
from rest_framework import serializers

from rest_api.models import ShortenedLink


class ShortenedURLSerializer(serializers.ModelSerializer):
    full_short_url = serializers.SerializerMethodField()
    short_code = serializers.CharField(required=False, max_length=50)

    class Meta:
        model = ShortenedLink
        fields = ["original_url", "short_code", "full_short_url", "visits", "user_ip"]
        read_only_fields = ["visits", "user_ip"]

    def get_full_short_url(self, obj: ShortenedLink) -> str:
        request = self.context.get("request")
        short_code_url = reverse("redirect", kwargs={"short_code": obj.short_code})
        return request.build_absolute_uri(short_code_url)
