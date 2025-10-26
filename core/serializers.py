from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['fn'] = user.first_name
        token['ln'] = user.last_name

        return token
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name",)
        read_only_fields = ("id",)

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_repleted = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password", "password_repleted")
        read_only_fields = ("id",)

    def validate(self, data):
        if data["password"] != data["password_repleted"]:
            raise serializers.ValidationError({"password_repleted": "Password fields didn't match."})
        data.pop("password_repleted", None)
        validate_password(data["password"], user=User(**data))
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user. password optional — set via set_password.
    """
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password_repleted = serializers.CharField(write_only=True, required=False, allow_blank=True, label="Confirm password")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_repleted")

    def validate(self, data):
        pw = data.get("password")
        pw2 = data.get("password_repleted")
        if pw or pw2:
            if pw != pw2:
                raise serializers.ValidationError({"password_repleted": "Password fields didn't match."})
            validate_password(pw, user=self.instance)
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_repleted", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance