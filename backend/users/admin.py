from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'email',
        'username'
    )