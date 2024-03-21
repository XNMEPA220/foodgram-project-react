from django_filters import rest_framework as filters

from foodgram.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        method='is_recipe_in_favorites_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_recipe_in_shopping_cart_filter')

    def is_recipe_in_favorites_filter(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user_id=self.request.user.id)
        return queryset

    def is_recipe_in_shopping_cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user_id=self.request.user.id)
        return queryset
# Можешь пожалуйста объяснить, почему нужно изменить функцию таким образом?
# Мы теперь не можем отфильтровать все рецепты, кроме избранных.
# Мне казалось, что раз у нас фильтр по полю,
# то мы при 1 должны получать все что true
# А при ?is_favorited=0, то все что false.
# Ну и соответственно, вообще без фильтра, если все рецепты.

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
