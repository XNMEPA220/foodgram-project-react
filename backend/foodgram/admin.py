from django.contrib import admin

from .models import Favorites, Follow, Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass
