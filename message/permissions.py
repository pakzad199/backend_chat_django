from rest_framework import permissions


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the sender to edit/delete a message.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
