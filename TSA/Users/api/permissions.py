from rest_framework.permissions import BasePermission
from Users.models import User


class IsProjectManagerOrSalesCreate(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        if request.method == 'POST':
            return user.area == User.PROJECT_MANAGEMENT or user.area == User.SALES
        else:
            return user.area == User.PROJECT_MANAGEMENT
