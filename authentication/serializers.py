from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    name = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Create a new user with hashed password."""
        name = validated_data.pop('name')
        email = validated_data['email']
        password = validated_data['password']

        # Use email as username (unique identifier)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )
        return user


class RegisterResponseSerializer(serializers.Serializer):
    """Response serializer for registration."""
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    email = serializers.EmailField()
    message = serializers.CharField()

    def get_name(self, obj):
        return obj.first_name


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
