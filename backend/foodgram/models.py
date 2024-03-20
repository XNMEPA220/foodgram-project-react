from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from backend.constants import (CHAR_SLUG_MODEL_MAX_LENGTH,
                               COLOR_MODEL_MAX_LENGTH)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=CHAR_SLUG_MODEL_MAX_LENGTH)
    color = ColorField('Цвет в НЕХ', max_length=COLOR_MODEL_MAX_LENGTH)
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=CHAR_SLUG_MODEL_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=CHAR_SLUG_MODEL_MAX_LENGTH)
    measurement_unit = models.CharField(
        'Мера измерения',
        max_length=CHAR_SLUG_MODEL_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='Уникальность ингредиентов'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=CHAR_SLUG_MODEL_MAX_LENGTH)
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to='foodgram/media'
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(1, message='Минимальное значение 1!'),
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Список тэгов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
        verbose_name='Ингридиенты'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='Уникальность ингредиентов в рецепте'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='Уникальность подписок'
            )
        ]

    def __str__(self):
        return f'Подписка пользователя {self.user} на {self.following}'


class AbstractModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='%(class)s_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        # related_name='%(class)s_recipe'
    )

    class Meta:
        abstract = True
        default_related_name = 'abstract'


class Favorites(AbstractModel):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Shopping_cart(AbstractModel):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (
            f'Рецепт {self.recipe} в списке покупок пользователя {self.user}'
        )
