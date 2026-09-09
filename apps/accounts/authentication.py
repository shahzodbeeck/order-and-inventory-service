from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from . import repositories
from .models import AuthUser


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if user_id is None:
            raise AuthenticationFailed("Token contains no recognizable user identification")

        user = repositories.get_user_by_id(user_id)
        if user is None:
            raise AuthenticationFailed("User not found")

        return AuthUser(id=user["id"], email=user["email"])
