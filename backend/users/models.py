from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserQueryset(models.QuerySet):

#     def add_user_annotations(self, user_id):
#         return self.annotate(
#             is_subscribed=models.Exists(
#                 Follow.objects.filter(user=user_id)
#             )
#         )


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    # user_with_annotations = UserQueryset.as_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


# class Follow(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='users'
#     )
#     following = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following'
#     )

#     class Meta:
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'following'],
#                 name='unique_name_following'
#             )
#         ]

#     def __str__(self):
#         return f'Подписка пользователя {self.user} на {self.following}'