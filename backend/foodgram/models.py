from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в НЕХ', max_length=7)
    slug = models.SlugField('Уникальный слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
    

class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Мера измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    image = models.CharField('Ссылка на картинку на сайте', max_length=1)
    text = models.TextField('Описание')
    cooking_time = models.PositiveIntegerField('Время приготовления в минутах')
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
        related_name='ingredient',
        verbose_name='Ингридиенты'
    ) 
    is_favorited = models.BooleanField('Находится ли в избранном')
    is_in_shopping_cart = models.BooleanField('Находится ли в корзине')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

