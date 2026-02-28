from django.contrib import admin
from .models import Post, PostDept


class PostDeptInline(admin.TabularInline):
    model = PostDept
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostDeptInline]
    list_display = ("title", "poster", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("title", "poster__username")
    readonly_fields = ("created_at", "updated_at")
