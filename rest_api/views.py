from django.http import HttpResponseRedirect
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ShortenedLink
from .serializers import ShortenedURLSerializer
from .utils import generate_short_code


class ShortenedURLCreateAPIView(generics.CreateAPIView):
    # TODO check for lazy loading
    queryset = ShortenedLink.objects.all()

    serializer_class = ShortenedURLSerializer

    def create(self, request, *args, **kwargs):
        original_url = request.data.get('original_url')
        # TODO: Add validation for the URL
        if not original_url:
            return Response({"error": "URL is required"}, status=400)

        short_url_obj, created = ShortenedLink.objects.get_or_create(original_url=original_url)
        if created:
            short_url_obj.short_code = generate_short_code()
            short_url_obj.user_ip = request.META.get('REMOTE_ADDR')
            short_url_obj.user_agent = request.META.get('HTTP_USER_AGENT')
            short_url_obj.save()

        serializer = self.get_serializer(short_url_obj, context={'request': request})
        return Response(serializer.data)


class RedirectToOriginalURLView(View):

    def get(self, request, short_code: ShortenedLink.short_code, *args, **kwargs):
        short_url_obj = get_object_or_404(ShortenedLink, short_code=short_code)
        short_url_obj.visits += 1
        short_url_obj.save()
        return HttpResponseRedirect(short_url_obj.original_url)
