from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


class IsAuthOrOwnerOrRead(BasePermission):
    """Пермишен для рецепта, разрешающий:
    Безопасные методы.
    Создание объектов, только авторизованному пользователю.
    Удаление и редактирование объектов только владельцу объекта.
    """
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST' or request.method == 'PATCH':
            return request.user.is_authenticated
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author and request.method == 'PATCH'

class IsOwnerAndReadOnly(BasePermission):
    """Пермишен, который разрешает только чтение для владельца объекта."""
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS and obj == request.user

class IsAuthenticated(BasePermission):
    """Проверяет, что пользователь аутентифицирован."""

    def has_permission(self, request, view):
        if not request.auth and not request.user.is_authenticated:
            raise AuthenticationFailed(
                detail='Учетные данные не были предоставлены.',
                code=status.HTTP_401_UNAUTHORIZED)
        return True

class IsProfileOwner(BasePermission):
    """Провяет, является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if request.user != obj:
            raise AuthenticationFailed(
                detail='Учетные данные не были предоставлены.',
                code=status.HTTP_401_UNAUTHORIZED)
        return True