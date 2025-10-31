from rest_framework import serializers
from message.models import Message, Attachment
from room.models import Room
from core.serializers import UserSerializer
from core.validators import validate_file as attachment_validate_file
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all()) is get from nested url

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'edited', 'deleted_at', 'created', 'modified']
        read_only_fields = ['id', 'sender', 'room', 'edited', 'deleted_at', 'created', 'modified']

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

class AttachmentSerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)
    uploaded_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attachment
        fields = ['id', 'message', 'file', 'uploaded_by', 'created']
        read_only_fields = ['id', 'message', 'uploaded_by', 'created']

    def get_uploaded_by(self, obj: Attachment):
        return obj.message.sender.username

    def validate_file(self, file):
        attachment_validate_file(file)
        return file

    def create(self, validated_data):
        return Attachment.objects.create(**validated_data)
