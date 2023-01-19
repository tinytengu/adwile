from rest_framework import permissions
from rest_framework.request import Request

from .models import Teaser


class IsOwnerOrAdmin(permissions.BasePermission):
    """Is the user owns an object or is a staff member."""

    def has_object_permission(self, request: Request, view, obj: Teaser):
        return request.user.is_staff or obj.author == request.user
