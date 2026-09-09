from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import services
from .models import AuthUser
from .serializers import LoginSerializer, RegisterSerializer, TokenPairResponseSerializer


def _issue_tokens(user_id, email) -> dict:
    refresh = RefreshToken.for_user(AuthUser(id=user_id, email=email))
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = services.register_user(**serializer.validated_data)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        tokens = _issue_tokens(user["id"], user["email"])
        return Response(TokenPairResponseSerializer(tokens).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.authenticate_user(**serializer.validated_data)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = _issue_tokens(user["id"], user["email"])
        return Response(TokenPairResponseSerializer(tokens).data, status=status.HTTP_200_OK)
