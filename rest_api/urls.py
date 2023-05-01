from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_api.views import (
    CreateShortenedURL,
    RedirectToOriginalURLView,
    UserShortenedURLListView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("create/", CreateShortenedURL.as_view(), name="create"),
    path("my-urls/", UserShortenedURLListView.as_view(), name="user-urls"),
    path("<str:short_code>/", RedirectToOriginalURLView.as_view(), name="redirect"),
]
