from rest_framework.permissions import BasePermission
from Users.models import User


class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.area == User.PROJECT_MANAGEMENT
