from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from .permissions import IsOwnerOrAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user signup, retrieve, update.
    - create (POST /api/users/) => signup (allow any)
    - retrieve, update, partial_update => owner or admin
    - list => admin only
    """
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_permissions(self):
        # create (signup) is open
        if self.action == "create":
            return [permissions.AllowAny()]

        # list only admins
        if self.action == "list":
            return [permissions.IsAdminUser()]

        # retrieve / update / partial_update use owner-or-admin
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    # Optional: expose an endpoint to get current logged-in user at /api/users/me/
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)
