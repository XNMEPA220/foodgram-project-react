from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password')
    def __str__(self):
        return self.username
