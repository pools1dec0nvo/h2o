from django.contrib import admin

from .models import Department, DeptMembership, SubTeam


class TeamLeaderInline(admin.TabularInline):
    model = DeptMembership
    verbose_name = "Team Leader"
    verbose_name_plural = "Team Leaders"
    fields = ("user", "role")
    readonly_fields = ("user", "role")
    extra = 0
    can_delete = False
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role=DeptMembership.Role.LEADER)

    def has_add_permission(self, request, obj=None):
        return False


class TeamMemberInline(admin.TabularInline):
    model = DeptMembership
    verbose_name = "Team Member"
    verbose_name_plural = "Team Members"
    fields = ("user", "role")
    autocomplete_fields = ("user",)
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role=DeptMembership.Role.MEMBER)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["role"].initial = DeptMembership.Role.MEMBER
        return formset


@admin.register(SubTeam)
class SubTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "dept", "slug")
    list_filter = ("dept",)
    search_fields = ("name", "portuguese_name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["dept"]
    fieldsets = (
        (None, {"fields": ("slug", "name", "portuguese_name", "dept")}),
        ("Appearance", {"fields": ("color",)}),
        ("Description", {"fields": ("description",)}),
    )


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
