from rest_framework import permissions

class IsMemberOrReadOnly(permissions.BasePermission):
    """
    Allow access only if user is a member. Safe methods could be allowed to authenticated users,
    or you can restrict everything to members.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
