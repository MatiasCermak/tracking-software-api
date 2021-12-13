from rest_framework.permissions import BasePermission, IsAuthenticated
from Users.models import User


class TicketModelViewsetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        if request.method == 'POST' or request.method == 'PATCH':
            return user.is_leader or user.area == User.PROJECT_MANAGEMENT
        elif request.method == 'DELETE':
            user.area == User.PROJECT_MANAGEMENT
        else:
            return IsAuthenticated.has_permission(request=request, view=view)


class TicketChangeStateViewSetPermissions(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        if request.method == 'PATCH':
            return user.is_leader or user.area == User.PROJECT_MANAGEMENT
