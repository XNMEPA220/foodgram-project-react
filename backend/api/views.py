from rest_framework import viewsets, status
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from foodgram.models import Tag, Ingredient, Recipe, Favorites, Follow, Shopping_cart
from users.models import User
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeCreateSerializer, MyUserSerializer, FavoriteSerializer, FollowSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=self.request.user)
        if queryset:
            return FollowSerializer
        return Response('Подписки отсутстуют', status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=('post', 'delete'))
    def subscribe(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == 'POST':
            if user == following:
                return Response('Нельзя подписаться на самого себя', status=status.HTTP_400_BAD_REQUEST)
            if follow.exists():
                return Response('Вы уже подписаны на него', status=status.HTTP_400_BAD_REQUEST)
            subscibe = Follow.objects.create(user=user, following=following)
            subscibe.save()
            return Response(f'Вы подписались на пользователя {follow}', status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            if follow.exists():
                follow.delete()
                return Response(f'Вы отписались от {following}', status=status.HTTP_204_NO_CONTENT)
            return Response(f'Вы не были подписаны на этого пользователя', status=status.HTTP_400_BAD_REQUEST)



class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer

    @action(methods=('post', 'delete'))
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorites.objects.filter(user=user, recipe=recipe).exists():
                return Response('Рецепт уже был добавлен в избранное', status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=('post', 'delete'))
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404
        if request.method == 'POST':
            if Shopping_cart.objects.filter(user=user, recipe=recipe).exists():
                return Response('Рецепт уже был добавлен в список покупок', status=status.HTTP_400_BAD_REQUEST)
            Shopping_cart.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            obj = Shopping_cart.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                'Рецепт не находится в списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )
