from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.users.view import UsersViewSet


router = DefaultRouter()
router.register('', UsersViewSet, basename='users')

urlpatterns = [
    
    path('', include(router.urls)),
]
