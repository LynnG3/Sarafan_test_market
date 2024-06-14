from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Проверяет, является ли текущий пользователь владельцем объекта.
    Запрещает чтение и др. действия с объектом другим пользователям.
    """
    def has_object_permission(self, request, view, obj):
        # Проверяем, что объект принадлежит текущему пользователю
        return obj.user == request.user


class IsAdminUserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )


class IsAdminUserOrReadonlyOrAddToCart(BasePermission):
    # def has_permission(self, request, view):
    #     if view.action == 'add_to_cart':
    #         return request.user.is_authenticated
    #     return (
    #         request.method in SAFE_METHODS
    #         or request.user
    #         and request.user.is_staff
    #     )

    def has_object_permission(self, request, view, obj):
        if view.action == 'add_to_cart':
            return obj.user == request.user
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
