from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'tags', TagViewSet, 'tags')
router.register(r'ingredients', IngredientViewSet, 'ingredients')
router.register(r'recipes', RecipeViewSet, 'recipes')
router.register(r'users', UserViewSet, 'users')

urlpatterns = (
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)