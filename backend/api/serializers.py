from collections import Counter

from django.db import transaction
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.constants import (
    ERROR_INGREDIENTS,
    ERROR_MESSAGE_DUBLICATE_INGREDIENTS,
    ERROR_MESSAGE_DUBLICATE_TAGS,
    ERROR_TAG,
    FOLLOWING_ERROR,
    IMAGE_ERROR,
    RECIPE_ADD_ERR0R,
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара пользователя."""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'subscribed',
            'avatar'
        )

    def get_subscribed(self, obj):
        """Метод проверки подписки."""
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user,
                following=obj
            ).exists()
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиент в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='name'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра рецепта."""

    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'favorite',
            'shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author', 'name', 'image', 'text', 'cooking_time')

    def check_recipe(self, obj, model):
        """Метод проверки связи рецепта и пользователя."""
        request = self.context.get('request')
        return bool(request
            and request.user.is_authenticated
            and model.objects.filter(
                user=request.user,
                recipe=obj
            ).exists())

    def get_ingredients(self, obj):
        """Метод получение ингредиентов для рецепта."""
        return obj.ingredients.value(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientrecipe__amount',)
        )

    def get_is_favorite(self, obj):
        """Метод проверки рецепта в избранном."""
        return self.check_recipe(obj, Favorite)

    def get_shopping_cart(self, obj):
        """Метод поверки рецепта в списке покупок."""
        return self.check_recipe(obj, ShoppingCart)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author',
        )

    def validate_tag_ingredient(self, value):
        """Валидатор проверки тега и ингредиентов."""
        tags = value.get('tags')
        ingredients = value.get('ingredients')

        field_errors = {}
        if not tags:
            field_errors['tags'] = ERROR_TAG
        elif dublicates := [str(tag) for tag, c in Counter(tags) if c > 1]:
            field_errors['tags'] = [
                ERROR_MESSAGE_DUBLICATE_TAGS.format(
                dublicates=", ".join(dublicates)
                )
        ]
        if not ingredients:
            field_errors['ingredients'] = ERROR_INGREDIENTS
        elif dublicates := [
            str(ingredient) for ingredient, c in Counter(ingredients) if c > 1
        ]:
            field_errors['ingredients'] = [
                ERROR_MESSAGE_DUBLICATE_INGREDIENTS.format(
                dublicates=", ".join(dublicates)
                )
            ]
        if field_errors:
            raise serializers.ValidationError(field_errors)
        return value

    def validate_image(self, value):
        """Валидатор изображения рецепта."""
        if not value:
            raise serializers.ValidationError(IMAGE_ERROR)
        return value

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_ingredients_recipe(recipe, ingredients, tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.ingredients.clear()
        self.add_tags_ingredients_recipe(instance, tags, ingredients)
        super().update(instance, validated_data)
        return instance

    def add_tags_ingredients_recipe(self, recipe, tags, ingredients):
        """Метод добавления тега и ингредиентов."""
        recipe.tags.set(tags)
        all_ingredients = []
        for ingredient in ingredients:
            ingredient_recipe = IngredientRecipe(
                name=ingredient.get('name'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )
            all_ingredients.append(ingredient_recipe)
        IngredientRecipe.objects.bulk_create(all_ingredients)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance, context=context).data


class RecipeInformation(serializers.ModelSerializer):
    """Сериализатор краткой информации о рецепте."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message=RECIPE_ADD_ERR0R
            ),
        )

    def to_representation(self, instance):
        return RecipeInformation(
            instance.recipe, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта в избранном."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже добавлен в избранное!'
            ),
        )

    def to_representation(self, instance):
        return RecipeInformation(
            instance.recipe, context=self.context).data


class SubscriptionSerializer(UserSerializer):
    """Сериализатор подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar'
        )

    def get_recipe(self, obj):
        """Метод получения рецепта."""
        return Recipe.objects.filter(author=obj)

    def get_list_recipes(self, obj):
        """Метод получения списка рецептов автора."""
        recipes = self.get_recipe(obj)
        recipes_limit = (self.context['request']
                         .query_params.get('recipes_limit'))
        if recipes_limit:
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                pass
        return RecipeInformation(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Метод получения количество рецептов."""
        return self.get_recipe(obj).count()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор получения списка рецептов автора."""

    class Meta:
        model = Subscription
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'following'),
                message=FOLLOWING_ERROR
            ),
        ]

    def validate_following(self, value):
        """Валидатор проверки подписки."""
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return value

    def to_representation(self, instance):
        return SubscriptionSerializer(
            instance.following, context=self.context).data
