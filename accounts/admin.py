from django.contrib import admin

from .models import Profile, Address


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "date_of_birth",
        "created_at",
    )

    search_fields = (
        "user__username",
        "phone_number",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "city",
        "state",
        "country",
        "is_default",
    )

    list_filter = (
        "country",
        "state",
        "is_default",
    )

    search_fields = (
        "full_name",
        "city",
        "phone_number",
    )