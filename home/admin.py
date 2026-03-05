from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import DeptMembership
from .models import User


class DeptMembershipInline(admin.TabularInline):
    model = DeptMembership
    extra = 1
    autocomplete_fields = ["dept"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [DeptMembershipInline]
    fieldsets = UserAdmin.fieldsets + (
        ("Role & Profile", {
            "fields": ("role", "linkedin_url", "phone_number", "profile_photo", "curriculum")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role & Profile", {
            "fields": ("role", "linkedin_url", "phone_number")
        }),
    )
    list_display = ("username", "email", "role", "is_staff", "is_superuser", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
