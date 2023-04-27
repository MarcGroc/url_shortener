from django.contrib import admin

from .models import ShortenedLink


@admin.register(ShortenedLink)
class ShortenedLinkAdmin(admin.ModelAdmin):
    list_display = (
        "original_url",
        "short_code",
        "created_at",
        "visits",
        "user_ip",
        "user_agent",
    )
    list_filter = ("created_at", "visits", "user_ip", "user_agent")
    search_fields = ("original_url", "short_code", "user_ip", "user_agent")
    search_help_text = "Search by original URL, short code, user IP or user agent"
    sortable_by = ("created_at", "visits", "user_ip", "user_agent")
    list_per_page = 25
