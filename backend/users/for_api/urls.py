from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
