from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from api.filters import IngredientFilter, RecipeFilter
from api.mixins import ListRetrieveViewSet
from api.pagination import PageLimitPagination
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    AvatarSerializer,
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)
from core.constants import NO_CONTENT, PREFIX_SHORT_LINK_RECIPE
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import  Subscription, User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination
    lookup_field = 'id'

    @action(
        detail=False,
        methods=['GET'],
        url_path="me",
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        detail=False,
        methods=('put',),
        url_path='me/avatar',
    )
    def update_avatar(self, request):
        serializer = AvatarSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @update_avatar.mapping.delete
    def delete_avatar(self, request):
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        followings = User.objects.filter(
            followings__user=request.user).prefetch_related('recipes')
        pages = self.paginate_queryset(followings)
        serializer = SubscriptionSerializer(
            pages, context={'request': request}, many=True
        )
        return self.get_paginated_response(serializer.data)

    def get_following(self):
        return get_object_or_404(User, id=self.kwargs.get('id'))

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        followings = User.objects.filter(
            followings__user=request.user).prefetch_related('recipes')
        pages = self.paginate_queryset(followings)
        serializer = SubscriptionSerializer(
            pages,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post',),
    )
    def subscribe(self, request, id=None):
        subscription_data = {
            'user': request.user.id,
            'following': get_object_or_404(User, id=id).id
        }
        serializer = FollowSerializer(
            data=subscription_data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        deleted_subscriptions, _ = Subscription.objects.filter(
            user=request.user,
            following=get_object_or_404(User, id=id)
        ).delete()
        if not deleted_subscriptions:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ListRetrieveViewSet):
    """Вьюсет тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецепта."""

    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination
    permission_classes = [IsAdminAuthorOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete',)
    lookup_field = 'id'

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    def add_recipe(self, request, serializer):
        data = {
            'user': request.user.id,
            'recipe': self.get_recipe().id
        }
        serializer = serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, request, model):
        deleted_recipes, _ = model.objects.filter(
            user=request.user,
            recipe=self.get_recipe()
        ).delete()
        if not deleted_recipes:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return RecipeReadSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=('get',),
        url_path='get-link',
    )
    def get_link(self, request):
        recipe = self.get_recipe()
        short_link = f'/{PREFIX_SHORT_LINK_RECIPE}{recipe.short_link}/'
        return Response(
            {'short-link': request.build_absolute_uri(short_link)},
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=('post',),
    )
    def shopping_cart(self, request):
        return self.add_recipe(request, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_recipe_from_shopping_cart(self, request):
        return self.delete_recipe(request, ShoppingCart)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Возвращает файл со списком покупок."""
        recipes = request.user.shopping_cart.all().values_list(
            'recipe', flat=True
        )

        if not recipes:
            return Response(
                {'detail': NO_CONTENT},
                status=status.HTTP_204_NO_CONTENT
            )

        ingredients = Ingredient.objects.filter(
            recipes__in=recipes
        ).values(
            'name',
            'ingredientrecipe__measurement_unit'
        ).annotate(amount=Sum('ingredientrecipe__amount'))

        shopping_cart = [
            f"{ing['name']} - "
            f"{ing['amount']}"
            f"{ing['ingredientrecipe__measurement_unit']}"
            for ing in ingredients
        ]

        shopping_cart_text = '\n'.join(shopping_cart)

        response = HttpResponse(shopping_cart_text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="my_shopping_cart.txt"')
        return response

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request):
        return self.add_recipe(request, FavoriteSerializer)

    @favorite.mapping.delete
    def delete_recipe_from_favorite(self, request):
        return self.delete_recipe(request, Favorite)


def redirect_to_recipe(request, short_link):
    recipe_id = get_object_or_404(Recipe, short_link=short_link).id
    return HttpResponseRedirect(
        request.build_absolute_uri(f'/recipes/{recipe_id}/'),
    )


