from django.contrib import admin
from .models import Post, Comment


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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "parent_body",
        "created",
        "updated",
        "is_reply",
        "short_body"
    )

    def short_body(self, obj):
        return obj.body[:50] + ('...' if len(obj.body) > 50 else '')
    short_body.short_description = 'Body'

    def parent_body(self, obj):
        if obj.parent:
            return obj.parent.body[:50] + ('...' if len(obj.parent.body) > 50 else '')
        return '-'
    parent_body.short_description = 'Parent Comment'

    list_filter = (
        'user',
    )

    search_fields = (
        "body",
        "user"
    )

    ordering = ("-created", "updated")


admin.site.register(Comment, CommentAdmin)