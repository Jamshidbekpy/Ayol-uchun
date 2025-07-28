from typing import ClassVar

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Interest, User, UserInterest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "is_deleted",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_deleted", "is_staff", "is_superuser")
    search_fields = ("email", "phone_number", "bio")
    ordering = ("-date_joined",)

    # create user form in admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )

    # change user form in admin
    fieldsets = (
        (None, {"fields": ("phone_number", "email", "password")}),
        ("Personal Info", {"fields": ("bio",)}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
        (
            "Deletion info",
            {"fields": ("is_deleted", "reason_delete_choices", "reason_delete_str")},
        ),
    )


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = ("id", "name")
    search_fields: ClassVar[tuple] = ("name",)


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display: ClassVar[tuple] = ("id", "user", "interest")
    search_fields: ClassVar[tuple] = ("user__email", "interest__name")
    autocomplete_fields: ClassVar[tuple] = ("user", "interest")
