from rest_framework import serializers

from django.contrib.auth import authenticate

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user details.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout endpoint.
    """
    refresh = serializers.CharField(help_text="Refresh token to blacklist")
