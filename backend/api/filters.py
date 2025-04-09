from distutils.util import strtobool
from django_filters import (
    AllValuesMultipleFilter,
    FilterSet,
    TypedChoiceFilter,
)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    """Фильтр для класса рецета."""

    favorited = TypedChoiceFilter(
        choices=((0, False), (1, True)),
        method='filter_favorited',
        coerce=strtobool,
        label='В избранном'
    )
    shopping_cart = TypedChoiceFilter(
        choices=((0, False), (1, True)),
        method='filter_shopping_cart',
        coerce=strtobool,
        label='В списке покупок'
    )
    tags = AllValuesMultipleFilter(field_name='tags__slug', label='Теги')

    class Meta:
        model = Recipe
        fields = ('author',)

    def filter_favorited(self, queryset, value):
        """Фильтр добавление в избранное."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, value):
        """Фильтр добавление в список покупок."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    """Фильтр для класса ингредиента."""

    search_param = 'name'