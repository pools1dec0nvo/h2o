from django.contrib import admin

from home.models import User, UserDeptOther
from .models import Department


class TeamLeaderInline(admin.TabularInline):
    model = User
    fk_name = "dept_main"
    verbose_name = "Team Leader"
    verbose_name_plural = "Team Leaders"
    fields = ("username", "first_name", "last_name", "email", "role")
    readonly_fields = ("username", "first_name", "last_name", "email", "role")
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


class TeamMemberInline(admin.TabularInline):
    model = UserDeptOther
    verbose_name = "Team Member"
    verbose_name_plural = "Team Members"
    fields = ("user",)
    autocomplete_fields = ("user",)
    extra = 1
    show_change_link = False


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "short_name", "portuguese_name", "color", "slug")
    search_fields = ("full_name", "portuguese_name", "slug")
    prepopulated_fields = {"slug": ("full_name",)}
    fieldsets = (
        (None, {"fields": ("slug", "full_name", "short_name", "portuguese_name")}),
        ("Appearance", {"fields": ("color",)}),
        ("Description", {"fields": ("description",)}),
    )
    inlines = [TeamLeaderInline, TeamMemberInline]
    ordering = ("full_name",)
