"""Configuration of the admin interface for MSMS"""
from django.contrib import admin
from lessons.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'is_active',
    ]
