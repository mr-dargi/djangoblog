from django.contrib import admin
from .models import Post


# Register Post in admin panel
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "published",
        "created_at",
        "updated_at",
        "is_premium"
    )

    list_filter = (
        'published',
    )

    search_fields = (
        "title",
        "author"
    )

    prepopulated_fields = {"slug": ("title", )}
    ordering = ("-published", "created_at")


admin.site.register(Post, PostAdmin)