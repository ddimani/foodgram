import uuid

from django.db import models, IntegrityError

from core.constants import (
    MAX_ATTEMPTS,
    MEASUREMENT_UNIT,
    NAME_MAX_LENGTH,
    SHORT_LINK_MAX_LENGTH,
    SLUG_MAX_LENGTH,
)
from core.validators import validator_amount, validator_cooking
from users.models import User


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название тега',
        help_text='Введите название тега'
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=MEASUREMENT_UNIT,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        ordering = ('name', 'measurement_unit',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'), name='unique_ingredient'
            ),
        )

    def __str__(self):
        return f'Ингредиент "{self.name}"'


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение рецепта',
        help_text='Выберите изображение для рецепта'
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        help_text='Введите описание для блюда'
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время для приготовления блюда',
        validators=[validator_cooking]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    short_link = models.CharField(
        max_length=SHORT_LINK_MAX_LENGTH,
        unique=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингридиенты',
    )

    class Meta:
        default_related_name = 'recipes'
        ordering = ('-pub_date', 'name')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def save(self, *args, **kwargs):
        if not self.short_link:
            for attempt in range(MAX_ATTEMPTS):
                try:
                    self.short_link = self.generate_short_link()
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    if attempt == MAX_ATTEMPTS - 1:
                        raise
                    pass
            else:
                super().save(*args, **kwargs)

    def generate_short_link(self):
        unique_id = str(uuid.uuid4())[:SHORT_LINK_MAX_LENGTH]
        return unique_id

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class IngredientRecipe(models.Model):
    """Модель ингредиент в рецепте."""

    name = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        validators=[validator_amount]
    )

    class Meta:
        ordering = ('name', 'recipe',)
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'name',
                ),
                name='unique_recipe_ingredient',
            ),
        )

    def __str__(self):
        return f'{self.name} - {self.name.measurement_unit}'


class FavoriteShoppingCart(models.Model):
    """Промежуточная модель рецепта избранного и в списке покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_user",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="%(class)s_user",
    )

    class Meta:
        abstract = True
        ordering = ['recipe']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(class)s_unique_recipe_user'
            )
        ]


class Favorite(FavoriteShoppingCart):
    """Модель рецепт в избранном."""

    class Meta:
        abstract = False
        default_related_name = 'favorites'
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'

    def __str__(self):
        return f'{self.recipe.name} в избранном {self.user.username}'


class ShoppingCart(FavoriteShoppingCart):
    """Модель рецепт в списке покупок."""

    class Meta:
        abstract = False
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self):
        return (
            f'Рецепт {self.recipe.name} в списке '
            f'покупок пользователя: {self.user.username}'
        )
