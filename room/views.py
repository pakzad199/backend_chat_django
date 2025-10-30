# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Room
from room.serializers import RoomSerializer
from room.permissions import IsMemberOrReadOnly

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsMemberOrReadOnly]

    def get_queryset(self):
        # Common pattern: only return rooms the user belongs to
        user = self.request.user
        return Room.objects.filter(members=user).distinct()

    def perform_create(self, serializer):
        # Optionally, add request.user to members automatically
        room = serializer.save(created_by=self.request.user, updated_by=self.request.user)
        # ensure creator is a member:
        room.members.add(self.request.user)
