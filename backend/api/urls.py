from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.recipe.view import TagViewSet, RecipeVievSet
from api.users.view import UsersViewSet
from api.ingredient.views import IngredientViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeVievSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]