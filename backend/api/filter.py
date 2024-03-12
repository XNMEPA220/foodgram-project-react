import django_filters
from django_filters import rest_framework as filters
from foodgram.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.filters.NumberFilter(
        method='is_recipe_in_favorites_filter')
    is_in_shopping_cart = django_filters.filters.NumberFilter(
        method='is_recipe_in_shoppingcart_filter')

    def is_recipe_in_favorites_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(furecipes__user_id=user.id)
        return queryset.exclude(furecipes__user_id=self.request.user.id)

    def is_recipe_in_shoppingcart_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(shoprecipe__user_id=user.id)
        return queryset.exclude(shoprecipe__user_id=self.request.user.id)

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
