from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from inira.app.accounts.infrastructure.docs.logout_docs import logout_docs
from inira.app.accounts.infrastructure.docs.register_docs import register_docs 
from inira.app.accounts.infrastructure.input.login_input_serializer import LoginInputSerializer
from inira.app.accounts.infrastructure.input.logout_input_serializer import LogoutInputSerializer
from inira.app.accounts.infrastructure.input.register_input_serializer import RegisterInputSerializer
from inira.app.accounts.infrastructure.input.update_profile_input_serializer import UpdateProfileInputSerializer
from inira.app.accounts.infrastructure.models import Profile
from inira.app.accounts.infrastructure.out.login_output_serializer import LoginOutputSerializer
from inira.app.accounts.infrastructure.out.user_output_serializer import UserOutputSerializer
from inira.app.accounts.infrastructure.docs.login_docs import login_docs
from inira.app.accounts.infrastructure.docs.update_profile_docs import update_profile_docs, get_profile_docs

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @login_docs
    def post(self, request, *args, **kwargs):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserOutputSerializer({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @register_docs
    def post(self, request, *args, **kwargs):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserOutputSerializer({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }).data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):

    permission_classes = [AllowAny]  # ← Verificar que esté así
    authentication_classes = []  # ← Agregar esta línea para deshabilitar completamente la autenticación

    @logout_docs
    def post(self, request, *args, **kwargs):
        serializer = LogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"detail": "Sesión cerrada exitosamente"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {"detail": "Token inválido o expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Error al cerrar sesión"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_profile_docs
    def get(self, request, *args, **kwargs):
        """Obtener perfil completo del usuario autenticado"""
        user = request.user
        
        user_data = UserOutputSerializer({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.profile.bio if hasattr(user, 'profile') else '',
            "avatar": user.profile.avatar if hasattr(user, 'profile') else None,
        }).data
        
        return Response(user_data, status=status.HTTP_200_OK)

    @update_profile_docs
    def patch(self, request, *args, **kwargs):
        """Actualizar perfil del usuario autenticado"""
        user = request.user
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        serializer = UpdateProfileInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.update(user, serializer.validated_data)
        user_data = UserOutputSerializer({
            "id": updated_user.id,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "bio": updated_user.profile.bio,
            "avatar": updated_user.profile.avatar,
        }).data
        
        return Response(user_data, status=status.HTTP_200_OK)
    

