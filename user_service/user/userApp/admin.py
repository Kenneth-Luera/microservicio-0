from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("role", "status")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": ("role", "status")
        }),
    )

    list_display = ("username", "email", "role", "status", "is_staff")
    list_filter = ("role", "status", "is_staff")
