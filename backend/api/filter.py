import django_filters
from django_filters import rest_framework as filters
from foodgram.models import Recipe

CHOICES = (
    (0, 'False'),
    (1, 'True'),
)

# class RecipeFilter(filters.FilterSet):
#     tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
#     is_favorited = django_filters.filters.NumberFilter(
#         method='is_recipe_in_favorites_filter')
#     is_in_shopping_cart = django_filters.filters.NumberFilter(
#         method='is_recipe_in_shopping_cart_filter')

#     def is_recipe_in_favorites_filter(self, queryset, name, value):
#         if value == 1:
#             user = self.request.user
#             return queryset.filter(favorites_recipe__user_id=user.id)
#         return queryset.exclude(favorites_recipe__user_id=self.request.user.id)

#     def is_recipe_in_shopping_cart_filter(self, queryset, name, value):
#         if value == 1:
#             user = self.request.user
#             return queryset.filter(shopping_cart_recipe__user_id=user.id)
#         return queryset.exclude(shopping_cart_recipe__user_id=self.request.user.id)

#     class Meta:
#         model = Recipe
#         fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.ChoiceFilter(choices=CHOICES, label='is_favorited')
    is_in_shopping_cart = filters.ChoiceFilter(choices=CHOICES)


    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
