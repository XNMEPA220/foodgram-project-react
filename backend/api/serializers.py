import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, validators

from foodgram.models import (Favorites, Follow, Ingredient, Recipe,
                             RecipeIngredient, Shopping_cart, Tag)
from users.models import User


class MyUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError(
            {'username': 'Пользователь с таким именем уже существует'}
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()


class MyCreateUserSerializer(MyUserSerializer):

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=('name', 'measurement_unit'),
                message='Тэг с таким названием уже существует'
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit'
        )
        validators = [
            validators.UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=('ingredient', 'amount'),
                message='Ингредиент с таким названием уже добавлен в рецепт'
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True)
    author = MyUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Shopping_cart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    ingredients = CreateIngredientInRecipeSerializer(many=True)

    def validate(self, value):
        if value.get('ingredients') is None:
            raise serializers.ValidationError(
                'Поле ингридиентов должно быть заполнено'
            )
        if value.get('tags') is None:
            raise serializers.ValidationError(
                'Поле тегов должно быть заполнено'
            )
        return value

    def validate_tags(self, value):
        tags_list = []
        if len(value) < 1:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один тег'
            )

        for tag in value:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги должны быть уникальными!'
                )
            tags_list.append(tag)
        return value

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        lst_ingredient = []

        for ingredient in ingredients:
            if ingredient['id'] in lst_ingredient:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными!'
                )
            lst_ingredient.append(ingredient['id'])
        if len(lst_ingredient) < 1:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент'
            )
        return value

    @staticmethod
    def create_ingredients(recipe, ingredients):
        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            )
            for ingredient in ingredients
        ]

        RecipeIngredient.objects.bulk_create(create_ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data, author=self.context.get('request').user
        )
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if ingredients:
            instance.ingredients.clear()
            self.create_ingredients(instance, ingredients)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'id'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeForFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(MyUserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.author.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeForFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        request = self.context.get('request')
        recipes = obj.author.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return recipes.count()


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )

    def validate(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )

        if Follow.objects.filter(
            user=data.get('user'),
            following=data.get('following')
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этот пользователь'
            )
        return data
