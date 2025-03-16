from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Кастомный пермишен, позволяющий редактировать и удалять объект только его
    автору.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsProfileOwner(BasePermission):
    """Провяет, является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if request.user != obj:
            raise AuthenticationFailed(
                detail='Учетные данные не были предоставлены.',
                code=status.HTTP_401_UNAUTHORIZED
            )
        return True
