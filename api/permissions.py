from rest_framework import permissions


class isOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object's creator is the same as the current user
        return obj.owner == request.user