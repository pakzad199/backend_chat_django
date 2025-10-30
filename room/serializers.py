from rest_framework import serializers
from room.models import Room
from django.contrib.auth import get_user_model
from core.serializers import UserSerializer

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    # Accept members as list of user IDs on input
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=True
    )

    # Show nested user info on read
    members_details = UserSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("id", "name", "is_group", "members", "members_details")
        read_only_fields = ("id", "members_details")

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        room = Room.objects.create(**validated_data)
        if members:
            room.members.set(members)
        return room

    def update(self, instance, validated_data):
        members = validated_data.pop("members", None)
        # update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If members provided, replace membership
        if members is not None:
            instance.members.set(members)

        return instance

    def validate(self, data):
        # Optional: enforce constraints, e.g. at least 2 members for a group
        if data.get('is_group') and len(data.get('members', [])) < 2:
            raise serializers.ValidationError("Group rooms must have at least 2 members.")
        return data
