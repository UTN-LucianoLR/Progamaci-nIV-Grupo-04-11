
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .services import MembershipService


class IsProjectAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Los métodos de lectura se permiten a los miembros.
        if request.method in SAFE_METHODS:
            return MembershipService.is_member(request.user, obj)

        # Las modificaciones solo se permiten a los administradores.
        project = obj if hasattr(obj, "memberships") else obj.project
        return MembershipService.is_admin(request.user, project)
