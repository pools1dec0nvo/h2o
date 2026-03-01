from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from .models import User, UserDeptOther


class UserDeptOtherInline(admin.TabularInline):
    model = UserDeptOther
    extra = 1
    max_num = 2
    autocomplete_fields = ["dept"]

    def clean(self):
        count = sum(1 for f in self.forms if f.cleaned_data and not f.cleaned_data.get("DELETE"))
        if count > 2:
            raise ValidationError("A user can have at most 2 other departments.")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserDeptOtherInline]
    autocomplete_fields = ["dept_main"]
    fieldsets = UserAdmin.fieldsets + (
        ("Role & Department", {
            "fields": ("role", "dept_main", "linkedin_url", "phone_number", "profile_photo")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role & Department", {
            "fields": ("role", "dept_main", "linkedin_url", "phone_number")
        }),
    )
    list_display = ("username", "email", "role", "dept_main", "is_staff", "is_active")
    list_filter = ("role", "dept_main", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
