from rest_framework import serializers
from django.urls import reverse
from .models import ShortenedLink


class ShortenedURLSerializer(serializers.ModelSerializer):
    full_short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedLink
        fields = ['original_url', 'full_short_url', 'visits']
        read_only_fields = ['visits']

    def get_full_short_url(self, obj):
        request = self.context.get('request')
        short_code_url = reverse('redirect', kwargs={'short_code': obj.short_code})
        return request.build_absolute_uri(short_code_url)