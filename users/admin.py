from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role",
            {"fields": ("role",)},
        ),
    )

    list_display = (
        "id",
        "username",
        "email",
        "role",
        "is_staff",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "city",
        "street",
        "house",
    )
