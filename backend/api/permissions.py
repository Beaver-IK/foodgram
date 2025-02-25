from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


class IsOwnerAndReadOnly(BasePermission):
    """Пермишен, который разрешает только чтение для владельца объекта."""
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS and obj == request.user

class ReadOnly(BasePermission):
    """Пермишен, разрешающий только чтение."""
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

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