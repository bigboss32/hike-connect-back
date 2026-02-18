# inira/app/shared/permissions.py

from functools import wraps
from rest_framework.exceptions import PermissionDenied


def require_group(*group_names):
    """Decorator que restringe un método de una APIView a grupos específicos."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            print(group_names)
            if not request.user.groups.filter(name__in=group_names).exists():
                raise PermissionDenied("No tienes permisos para realizar esta acción.")
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
