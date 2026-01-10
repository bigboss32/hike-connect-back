
from rest_framework.permissions import BasePermission

class HasGroupPermission(BasePermission):
    """
    Permite acceso solo a usuarios autenticados que pertenezcan
    a ciertos grupos, definidos globalmente o por método HTTP.
    """

    allowed_groups = []          
    method_groups = {}         

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        user_groups = set(user.groups.values_list('name', flat=True))
        method = request.method.upper()
        if self.method_groups and method in self.method_groups:
            return bool(user_groups.intersection(set(self.method_groups[method])))
        if self.allowed_groups:
            return bool(user_groups.intersection(set(self.allowed_groups)))
        return True
