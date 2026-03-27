from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import UserProfile

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own profile
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = user.profile
            # Generate verification token
            token = PasswordResetTokenGenerator().make_token(user)
            profile.email_verification_token = token
            profile.save()

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            # Create verification link
            verification_link = f"{settings.FRONTEND_URL}/verify-email/?uidb64={uidb64}&token={token}"

            # Send verification email
            subject = 'Verify Your Email'
            message = f"""
            Hi {user.username},
            
            Please verify your email by clicking the link below:
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
                return Response(
                    {
                        'message': 'User registered successfully. Check your email to verify your account.',
                        'user': UserSerializer(user).data,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                user.delete() # delete user if email fails
                return Response(
                    {'error': 'Failed to send verification email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login user - requires email verification"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(username=username)

                # Check if email is verified
                if not user.profile.email_verified:
                    return Response(
                        {'error': 'Please verify your email before logging in'},
                        status=status.HTTP_403_FORBIDDEN
                    )

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

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """Verify email using token from email"""
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')

        if not uidb64 or not token:
            return Response(
                {'error': 'Missing uidb64 or token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            profile = user.profile

            # Verify token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark email as verified
            profile.email_verified = True
            profile.email_verification_token = None
            profile.save()

            return Response(
                {'message': 'Email verified successfully. You can now login.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Invalid token or user'},
                status=status.HTTP_400_BAD_REQUEST
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

            # Create reset link
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

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        """Reset password using token from email"""
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['password']

            try:
                # Decode user ID
                user_id = smart_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=user_id)

                # Verify token
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response(
                        {'error': 'Invalid or expired token'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Reset password
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

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
