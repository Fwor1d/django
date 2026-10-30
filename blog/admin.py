from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("author", "created_at")
    fields = ("author", "text", "created_at")
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "author", "created_at", "is_published")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "body", "summary")
    readonly_fields = ("created_at", "updated_at")
    inlines = [CommentInline]

    def save_model(self, request, obj, form, change):
        if obj.author_id is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "text", "post__title")
