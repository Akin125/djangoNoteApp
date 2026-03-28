from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.utils.encoding import force_bytes, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'username': {'help_text': 'The username for the account'},
            'email': {'help_text': 'The email address associated with the account'},
            'first_name': {'help_text': 'User\'s first name'},
            'last_name': {'help_text': 'User\'s last name'},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email_verified',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='Password must be at least 8 characters long'
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='Confirm password - must match password field'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {
                'help_text': 'Username for the account (must be unique)',
                'required': True,
            },
            'email': {
                'help_text': 'Email address (must be unique and valid)',
                'required': True,
            },
            'first_name': {
                'help_text': 'First name (optional)',
                'required': False,
            },
            'last_name': {
                'help_text': 'Last name (optional)',
                'required': False,
            },
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        help_text='Username for login'
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        help_text='Password for login'
    )

    class Meta:
        fields = ('username', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Current password'
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        help_text='New password (minimum 8 characters)'
    )
    new_confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        help_text='Confirm new password - must match new_password'
    )

    def validate(self, data):
        if data['new_password'] != data['new_confirm_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match'})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'new_password': 'New password cannot be same as old password'})
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
        help_text='Email address associated with your account'
    )

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='New password (minimum 8 characters)'
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text='Confirm new password - must match password'
    )
    uidb64 = serializers.CharField(
        write_only=True,
        help_text='User ID encoded in base64 (from reset email link)'
    )
    token = serializers.CharField(
        write_only=True,
        help_text='Password reset token (from reset email link)'
    )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data