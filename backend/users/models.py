from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from backend.constants import USER_MODEL_MAX_LENGTH


class User(AbstractUser):

    username = models.CharField(
        'Логин',
        max_length=USER_MODEL_MAX_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True
    )
    first_name = models.CharField(
        max_length=USER_MODEL_MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=USER_MODEL_MAX_LENGTH,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_username'
            )
        ]

    def __str__(self):
        return self.username
