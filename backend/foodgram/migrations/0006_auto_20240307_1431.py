# Generated by Django 3.2 on 2024-03-07 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0005_recipe_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.BooleanField(blank=True, default=False, verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.BooleanField(blank=True, default=False, verbose_name='Список покупок'),
        ),
    ]
