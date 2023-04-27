from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import RedirectToOriginalURLView, ShortenedURLCreateAPIView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", ShortenedURLCreateAPIView.as_view(), name="shortened-link-create"),
    path("<str:short_code>/", RedirectToOriginalURLView.as_view(), name="redirect"),
]
