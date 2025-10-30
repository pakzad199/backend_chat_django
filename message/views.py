from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from message.models import Message
from room.models import Room
from message.serializers import MessageSerializer
from message.permissions import IsSenderOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsSenderOrReadOnly]

    def get_queryset(self):
        room_id = self.kwargs.get('room_pk')  # assuming nested route: /rooms/<room_pk>/messages/
        return Message.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_pk')
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise PermissionDenied("Room not found")

        # Ensure the user is a member of the room
        if not room.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You are not a member of this room")

        serializer.save(room=room, sender=self.request.user, created_by=self.request.user, updated_by=self.request.user)
