from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework.response import Response

from rest_api.models import ShortenedLink
from rest_api.serializers import ShortenedURLSerializer
from rest_api.tasks import create_shortened_url
from rest_api.utils import is_valid_url


@method_decorator(cache_page(300), name="post")
class CreateShortenedURL(generics.CreateAPIView):
    """
    View for creating a shortened URL, validates the URL, returns the shortened URL and collects the user's IP and
    user agent.
    """

    queryset = ShortenedLink.objects.all()

    serializer_class = ShortenedURLSerializer

    @method_decorator(ratelimit(key="ip", rate="12/m", method="GET", block=True))
    def create(self, request, *args, **kwargs):
        original_url = request.data.get("original_url")
        if not original_url or not is_valid_url(original_url):
            return Response(
                {
                    "error": "URL is invalid, example URL https://en.wikipedia.org/wiki/URL"
                },
                status=400,
            )

        custom_short_code = request.data.get("short_code")
        user_ip = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")

        result = create_shortened_url.delay(
            original_url, user_ip, user_agent, custom_short_code
        ).get()

        if isinstance(result, dict) and "error" in result:
            return Response(
                {"error": result["error"], "original_url": original_url},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # short_url_id = result["id"]
        short_url = ShortenedLink.objects.get(id=result)
        serializer = self.get_serializer(short_url, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(cache_page(300), name="get")
class UserShortenedURLListView(generics.ListAPIView):
    """
    View for listing the user's shortened URLs, based on the user's IP. Not works correctly if user has dynamic IP.
    """

    serializer_class = ShortenedURLSerializer

    def get_queryset(self, *args, **kwargs):
        user_ip = self.request.META.get("REMOTE_ADDR")
        return ShortenedLink.objects.filter(user_ip=user_ip)


@method_decorator(cache_page(300), name="dispatch")
class RedirectToOriginalURLView(View):
    """
    View for redirecting the user to the original URL, increments the visits counter.
    """

    @method_decorator(ratelimit(key="ip", rate="12/m", method="GET", block=True))
    def get(self, request, short_code: ShortenedLink.short_code, *args, **kwargs):
        short_url = get_object_or_404(ShortenedLink, short_code=short_code)
        short_url.visits += 1
        short_url.save()
        return HttpResponseRedirect(short_url.original_url)
