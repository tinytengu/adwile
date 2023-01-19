from django.contrib import admin

from .models import Teaser


@admin.register(Teaser)
class TeaserAdmin(admin.ModelAdmin):
    # List
    list_display = [
        "id",
        "title",
        "author",
        "description",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status"]

    # Fields
    readonly_fields = ["id", "created_at", "updated_at"]
    search_fields = ["id", "title", "author__username", "description"]
    fieldsets = (
        (
            None,
            {
                "fields": ("id", "title", "author", "status", "description"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj: Teaser = None):
        """Makes `status` field read-only on create and after changing from `pending`"""
        if not obj or (obj and obj.status != Teaser.Status.PENDING):
            return self.readonly_fields + ["status"]

        return self.readonly_fields
