from rest_framework.permissions import BasePermission
from Users.models import User


class IsSalesOnly(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        return user.area == User.SALES
