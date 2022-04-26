from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": ("email", "first_name", "last_name", "affiliation", "password")},
        ),
        (
            "Permissions",
            {"fields": ("agencies", "is_staff", "is_superuser", "is_active")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "affiliation",),
            },
        ),
        ("Permissions", {"fields": ("agencies", "is_staff", "is_superuser")},),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def get_form(self, request, *args, **kwargs):
        form = super(UserAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form
