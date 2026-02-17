from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from inira.app.shared.email.email_service import (
    send_password_reset_email,
    send_verification_email,
)
from inira.app.shared.utils import generate_email_code
from inira.app.accounts.infrastructure.models import (
    EmailVerification,
    PasswordReset,
    Profile,
    User,
)
from inira.app.accounts.infrastructure.input import *

from inira.app.accounts.infrastructure.docs import *


@login_docs
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        roles = list(user.groups.values_list("name", flat=True))
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "roles": roles,
            }
        )


@register_docs
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        code = generate_email_code()

        EmailVerification.objects.update_or_create(
            user=user,
            defaults={"code": code, "verified": False},
        )

        send_verification_email(user.email, code)

        return Response(
            {"message": "Cuenta creada. Revisa tu correo para verificarlo."},
            status=status.HTTP_201_CREATED,
        )


@verify_email_docs
class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        verification = (
            EmailVerification.objects.select_related("user")
            .filter(
                user__email=email,
                verified=False,
            )
            .first()
        )

        if not verification or verification.code != code:
            return Response({"detail": "Código inválido"}, status=400)

        if timezone.now() > verification.created_at + timedelta(minutes=10):
            return Response(
                {"detail": "Código expirado. Solicita uno nuevo."}, status=400
            )

        user = verification.user
        user.profile.correo_electronico_confirmado = True
        user.save()

        verification.verified = True
        verification.save()

        return Response({"message": "Correo verificado correctamente"})


@resend_verification_docs
class ResendVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        verification = EmailVerification.objects.filter(
            user__email=email,
            verified=False,
        ).first()

        if not verification:
            return Response({"detail": "No hay verificación pendiente."}, status=400)

        code = generate_email_code()

        verification.code = code
        verification.created_at = timezone.now()
        verification.save()

        send_verification_email(email, code)

        return Response({"message": "Código reenviado correctamente"})


@update_profile_docs
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.profile.bio if hasattr(user, "profile") else "",
                "avatar": user.profile.avatar if hasattr(user, "profile") else None,
            }
        )

    def patch(self, request):
        user = request.user

        if not hasattr(user, "profile"):
            Profile.objects.create(user=user)

        serializer = UpdateProfileInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_user = serializer.update(user, serializer.validated_data)

        return Response(
            {
                "id": updated_user.id,
                "email": updated_user.email,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "bio": updated_user.profile.bio,
                "avatar": updated_user.profile.avatar,
            }
        )


@logout_docs
class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Sesión cerrada correctamente"},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except TokenError:
            return Response(
                {"detail": "Token inválido o expirado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            return Response(
                {"detail": "Error al cerrar sesión"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@request_password_reset_docs
class RequestPasswordResetAPIView(APIView):
    """
    Envía código de recuperación de contraseña al email del usuario
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        # Generar código
        code = generate_email_code()

        # Crear o actualizar el registro de recuperación
        PasswordReset.objects.update_or_create(
            user=user,
            defaults={"code": code, "verified": False},
        )

        # Enviar email
        send_password_reset_email(email, code)

        return Response(
            {"message": "Código enviado a tu correo electrónico"},
            status=status.HTTP_200_OK,
        )


@verify_password_reset_code_docs
class VerifyPasswordResetCodeAPIView(APIView):
    """
    Verifica que el código de recuperación sea válido
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyPasswordResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        # Buscar el código de recuperación
        reset = (
            PasswordReset.objects.select_related("user")
            .filter(
                user__email=email,
                verified=False,
            )
            .first()
        )

        if not reset or reset.code != code:
            return Response({"detail": "Código inválido"}, status=400)

        if timezone.now() > reset.created_at + timedelta(minutes=10):
            return Response(
                {"detail": "Código expirado. Solicita uno nuevo."}, status=400
            )

        return Response({"message": "Código válido"}, status=status.HTTP_200_OK)


@reset_password_docs
class ResetPasswordAPIView(APIView):
    """
    Establece nueva contraseña usando el código de recuperación
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        password = serializer.validated_data["password"]

        # Buscar el código de recuperación
        reset = (
            PasswordReset.objects.select_related("user")
            .filter(
                user__email=email,
                verified=False,
            )
            .first()
        )

        if not reset or reset.code != code:
            return Response({"detail": "Código inválido"}, status=400)

        if timezone.now() > reset.created_at + timedelta(minutes=10):
            return Response(
                {"detail": "Código expirado. Solicita uno nuevo."}, status=400
            )

        # Actualizar contraseña
        user = reset.user
        user.set_password(password)
        user.save()

        # Marcar el código como usado
        reset.verified = True
        reset.save()

        return Response(
            {"message": "Contraseña actualizada correctamente"},
            status=status.HTTP_200_OK,
        )
