from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    # ========== AUTH ENDPOINTS ==========

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account and send email verification link.",
        request=RegisterSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user and return tokens"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = user.profile

            # Generate verification token
            token = PasswordResetTokenGenerator().make_token(user)
            profile.email_verification_token = token
            profile.save()

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            verification_link = f"{settings.FRONTEND_URL}/verify-email/?uidb64={uidb64}&token={token}"

            # Send verification email
            subject = 'Verify Your Email'
            message = f"""
Hi {user.username},

Click the link below to verify your email and activate your account:
{verification_link}

This link will expire in 24 hours.
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                # Generate tokens
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        'message': 'User registered successfully. Check your email to verify your account.',
                        'user': UserSerializer(user).data,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                user.delete()
                return Response(
                    {'error': 'Failed to send verification email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Login user",
        description="Authenticate user and get JWT tokens.",
        request=LoginSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login user and return tokens"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(username=username)

                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            'message': 'Login successful',
                            'user': UserSerializer(user).data,
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get user profile",
        description="Retrieve the profile of the authenticated user.",
        responses=UserSerializer,
    )
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Request password reset",
        description="Send password reset email to the specified email address.",
        request=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        """Request password reset email"""
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Generate reset token
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/?uidb64={uidb64}&token={token}"

            # Send email
            subject = 'Password Reset Request'
            message = f"""
Hi {user.username},

Click the link below to reset your password:
{reset_link}

This link will expire in 24 hours.

If you did not request this, please ignore this email.
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response(
                    {'message': 'Password reset link sent to your email'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to send email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Reset password",
        description="Reset password using token from password reset email.",
        request=ResetPasswordSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        """Reset password using token from email"""
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['password']

            try:
                user_id = smart_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=user_id)

                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response(
                        {'error': 'Invalid or expired token'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user.set_password(new_password)
                user.save()

                return Response(
                    {'message': 'Password reset successfully. You can now login with your new password.'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': 'Invalid token or user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Change password",
        description="Change password for the authenticated user.",
        request=ChangePasswordSerializer,
    )
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change password for authenticated user"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Wrong password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete user account",
        description="Permanently delete the authenticated user account.",
    )
    @action(detail=False, methods=['delete'])
    def delete_account(self, request):
        """Delete authenticated user account permanently"""
        user = request.user
        username = user.username
        user.delete()
        return Response(
            {'message': f'User account {username} has been deleted successfully'},
            status=status.HTTP_200_OK
        )
