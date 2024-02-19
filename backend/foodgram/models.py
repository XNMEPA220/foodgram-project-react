from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в НЕХ', max_length=7)
    slug = models.SlugField('Уникальный слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
