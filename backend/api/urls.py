from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.ingredient.views import IngredientViewSet
from api.recipe.view import RecipeVievSet, TagViewSet
from api.users.view import UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeVievSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
