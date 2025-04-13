from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Пермишн проверки доступа."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_superuser