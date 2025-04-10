from django.contrib import admin

from core.constants import EMPTY_VALUE_ADMIN_PANEL
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


admin.site.empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ панель для модели тег."""

    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ панель для модели ингредиент."""

    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    """Админ панель для управления ингредиента в рецепте."""

    model = IngredientRecipe
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ панель для модели рецепт."""

    inlines = (IngredientRecipeInline,)
    list_display = ('name', 'author', 'count_is_favorited')
    search_fields = ('author__username', 'name')
    list_filter = ('tags',)

    @admin.display(description='Количество добавлений в избранное')
    def count_is_favorited(self, obj):
        return obj.favorites.count()


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админ панель для модели ингредиент в рецепте."""

    list_display = ('id', 'name', 'recipe', 'amount')
    list_editable = ('name', 'recipe', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админ панель для модели рецепт в избранном."""

    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    """Админ панель для модели рецепт в списке покупок."""
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')
