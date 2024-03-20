from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
        'followers',
        'recipes'
    )
    list_filter = (
        'email',
        'username'
    )

    def followers(self, obj):
        return obj.users.count()

    def recipes(self, obj):
        return obj.author.all().count()
