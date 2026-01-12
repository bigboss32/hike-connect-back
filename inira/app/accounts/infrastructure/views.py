from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from inira.app.accounts.infrastructure.docs.register_docs import register_docs 
from inira.app.accounts.infrastructure.input.login_input_serializer import LoginInputSerializer
from inira.app.accounts.infrastructure.input.register_input_serializer import RegisterInputSerializer
from inira.app.accounts.infrastructure.out.login_output_serializer import LoginOutputSerializer
from inira.app.accounts.infrastructure.out.user_output_serializer import UserOutputSerializer
from inira.app.accounts.infrastructure.docs.login_docs import login_docs


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