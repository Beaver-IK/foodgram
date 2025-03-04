from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status


class Base(BasePermission):
    
    OWNER_METHODS = ('POST', 'PATCH', 'DELETE')
    auth_fail = AuthenticationFailed(
                detail='Учетные данные не были предоставлены.',
                code=status.HTTP_401_UNAUTHORIZED)

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
        return (request.user == obj.author and 
                request.method in self.OWNER_METHODS)

class IsOwnerAndReadOnly(Base):
    """Пермишен, который разрешает только чтение для владельца объекта."""
    
    def has_permission(self, request, view):
        if not request.method in SAFE_METHODS:
            raise self.auth_fail
        return True

    def has_object_permission(self, request, view, obj):
        if not request.method in SAFE_METHODS and not obj == request.user:
            raise self.auth_fail
        return True

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