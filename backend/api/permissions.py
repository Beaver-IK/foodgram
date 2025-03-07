from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS, BasePermission


class Base(BasePermission):
    """Базовый класс с методами владельца объекта и ошибкой авутентификации."""
    OWNER_METHODS = ('POST', 'PATCH', 'DELETE')
    auth_fail = AuthenticationFailed(
        detail='Учетные данные не были предоставлены.',
        code=status.HTTP_401_UNAUTHORIZED
    )


class IsAuthOrOwnerOrRead(Base):
    """Пермишен для рецепта, разрешающий:
    Безопасные методы.
    Создание объектов, только авторизованному пользователю.
    Удаление и редактирование объектов только владельцу объекта.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in self.OWNER_METHODS:
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user == obj.author
                and request.method in self.OWNER_METHODS)


class IsAuthenticated(Base):
    """Проверяет, что пользователь аутентифицирован."""

    def has_permission(self, request, view):
        if not request.auth and not request.user.is_authenticated:
            raise self.auth_fail
        return True


class IsProfileOwner(Base):
    """Провяет, является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if request.user != obj:
            raise self.auth_fail
        return True
