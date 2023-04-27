from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import ShortenedLink
from .serializers import ShortenedURLSerializer
from .tasks import create_shortened_url


class ShortenedURLCreateAPIView(generics.CreateAPIView):
    """
    View for creating a shortened URL, validates the URL, returns the shortened URL and collects the user's IP and
    user agent.
    """

    queryset = ShortenedLink.objects.all()

    serializer_class = ShortenedURLSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="original_url",
                description="URL to be shortened",
                required=True,
                type=str,
            )
        ],
        responses={200: ShortenedURLSerializer},
    )
    def create(self, request, *args, **kwargs):
        original_url = request.data.get("original_url")
        validate_url = URLValidator()

        try:
            validate_url(original_url)
        except ValidationError:
            return Response(
                {
                    "error": "URL is invalid, example URL https://en.wikipedia.org/wiki/URL"
                },
                status=400,
            )

        if not original_url:
            return Response({"error": "URL is required"}, status=400)

        user_ip = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")

        short_url_id = create_shortened_url.delay(
            original_url, user_ip, user_agent
        ).get()
        short_url = ShortenedLink.objects.get(id=short_url_id)
        serializer = self.get_serializer(short_url, context={"request": request})
        return Response(serializer.data)


class RedirectToOriginalURLView(View):
    """
    View for redirecting the user to the original URL, increments the visits counter.
    """

    def get(self, request, short_code: ShortenedLink.short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortenedLink, short_code=short_code)
        short_url.visits += 1
        short_url.save()
        return HttpResponseRedirect(short_url.original_url)
