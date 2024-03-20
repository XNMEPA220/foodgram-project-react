from django.contrib import admin

from .models import (Favorites, Follow, Ingredient, Recipe, RecipeIngredient,
                     Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # readonly_fields = ('pub_date',)
    list_display = (
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
        'favorites')
    list_filter = (
        'name',
        'author',
        'tags'
    )
    filter_horizontal = ('tags',)
    inlines = [
        RecipeIngredientInline,
    ]

    def favorites(self, obj):
        return obj.favorites_recipe.count()


class IngredientRecipeInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass
