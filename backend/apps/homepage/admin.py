from django.contrib import admin

from apps.homepage.models import ServiceLink


@admin.register(ServiceLink)
class ServiceLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "sort_order", "is_visible", "created_at")
    list_filter = ("category", "is_visible")
    search_fields = ("title", "url", "description")
    ordering = ("sort_order", "created_at")
