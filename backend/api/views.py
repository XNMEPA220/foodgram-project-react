import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from foodgram.models import (
    Favorites,
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Shopping_cart,
    Tag
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .filter import RecipeFilter
from .paginator import MyPagination
from .permission import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, MyUserSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = MyPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(
            detail=False,
            permission_classes=(permissions.IsAuthenticated,)
        )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=self.request.user)
        if queryset:
            pages = self.paginate_queryset(queryset)
            seralizer = FollowSerializer(
                pages,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(seralizer.data)
        return Response(
            'Подписки отсутстуют',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
            methods=('post', 'delete'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,)
        )
    def subscribe(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == 'POST':
            if user == following:
                return Response(
                    'Нельзя подписаться на самого себя',
                    status=status.HTTP_400_BAD_REQUEST
                )
            if follow.exists():
                return Response(
                    'Вы уже подписаны на него',
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscibe = Follow.objects.create(user=user, following=following)
            subscibe.save()
            queryset = User.objects.filter(following__user=self.request.user)
            pages = self.paginate_queryset(queryset)
            seralizer = FollowSerializer(
                pages,
                many=True,
                context={'request': request}
            )
            return Response(seralizer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if follow.exists():
                follow.delete()
                return Response(
                    f'Вы отписались от {following}',
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                'Вы не были подписаны на этого пользователя',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        return super().me(request)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = MyPagination
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update', 'update'):
            return RecipeCreateSerializer

    @action(
            methods=('post', 'delete'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,)
        )
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                return Response(
                    'Рецепт не найден',
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite = Favorites.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                return Response(
                    'Рецепт уже был добавлен в избранное',
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = Favorites.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(
                    'Рецепт удален из избранного',
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                'Данный рецепт не был добавлен в избранное',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
            methods=('post', 'delete'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,)
        )
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                return Response(
                    'Рецепт не найден',
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Shopping_cart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    'Рецепт уже был добавлен в список покупок',
                    status=status.HTTP_400_BAD_REQUEST
                )
            Shopping_cart.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            obj = Shopping_cart.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                'Рецепт не находится в списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        pfile = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
        pfile.setFont('DejaVu', 12)
        pfile.drawString(100, 750, 'Список покупок')
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoprecipe__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            sum=Sum('amount')
        )
        y = 700
        for item in ingredients:
            pfile.drawString(
                100, y,
                f'{item["ingredient__name"]}'
                f'({item["ingredient__measurement_unit"]}) - '
                f'{item["sum"]}'
            )
            y -= 20

        pfile.showPage()
        pfile.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.pdf'
        )
