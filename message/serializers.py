from rest_framework import serializers
from message.models import Message
from room.models import Room
from core.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'edited', 'deleted_at', 'created', 'modified']
        read_only_fields = ['id', 'sender', 'edited', 'deleted_at', 'created', 'modified']

    def create(self, validated_data):
        """
        Create a message with the current user as sender and a given room.
        """

        message = Message.objects.create(
            **validated_data
        )
        return message

    def update(self, instance: Message, validated_data):
        """
        Update the message — mark as edited if content changes.
        """
        new_content = validated_data.get('content', instance.content)
        if new_content != instance.content:
            instance.edited = True
        instance.content = new_content
        instance.save()
        return instance

    def delete(self, instance: Message):
        """
        Soft delete the message.
        """
        instance.deleted_at = True
        instance.save()
        return instance