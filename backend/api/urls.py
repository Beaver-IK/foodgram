from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.recipe.view import TagViewSet
from api.users.urls import UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tag')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]