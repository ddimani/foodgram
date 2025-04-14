from distutils.util import strtobool
from django_filters import (
    AllValuesMultipleFilter,
    FilterSet,
    TypedChoiceFilter,
)
from rest_framework.filters import SearchFilter

from core.constants import RECIPE_FILTER_CHOICES
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = TypedChoiceFilter(
        choices=RECIPE_FILTER_CHOICES,
        method='filter_is_favorited',
        coerce=strtobool
    )
    is_in_shopping_cart = TypedChoiceFilter(
        choices=RECIPE_FILTER_CHOICES,
        method='filter_is_in_shopping_cart',
        coerce=strtobool
    )
    tags = AllValuesMultipleFilter(field_name='tags__slug', )

    class Meta:
        model = Recipe
        fields = ('author',)

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppingcart_recipe__user=self.request.user)


class IngredientFilter(SearchFilter):
    """Фильтр для класса ингредиента."""

    search_param = 'name'
