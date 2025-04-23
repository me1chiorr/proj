from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

class IsAuthenticated401(BasePermission):
    """
    Как IsAuthenticated, но при отсутствии аутентификации
    бросает NotAuthenticated -> HTTP 401.
    """
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            raise NotAuthenticated('Требуется аутентификация.')
        return True
