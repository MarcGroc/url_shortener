from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import ShortenedURLCreateAPIView, RedirectToOriginalURLView

router = DefaultRouter()
# TODO: add router for the API
# router.register(r"shorten", ShortenedURLCreateAPIView, basename="shorten")
# router.register(r"redirect", RedirectToOriginalURLView, basename="redirect")
urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # path("", include(router.urls)),
    path("shorten/", ShortenedURLCreateAPIView.as_view(), name="shorten"),
    path('<str:short_code>/', RedirectToOriginalURLView.as_view(), name='redirect'),
]
