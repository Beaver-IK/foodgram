from rest_framework.permissions import SAFE_METHODS, BasePermission


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
    
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
