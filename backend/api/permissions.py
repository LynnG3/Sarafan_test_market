from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Проверяет, является ли текущий пользователь владельцем объекта.
    Запрещает доступ к объекту на удаление и изменение другим пользователям.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.user == request.user
        )


class IsOwner(BasePermission):
    """
    Проверяет, является ли текущий пользователь владельцем объекта.
    Запрещает чтение и др. действия с объектом другим пользователям.
    """
    def has_object_permission(self, request, view, obj):
        # Проверяем, что объект принадлежит текущему пользователю
        return obj.user == request.user


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
