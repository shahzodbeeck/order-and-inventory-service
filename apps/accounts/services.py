from django.contrib.auth.hashers import check_password, make_password

from . import repositories


def register_user(email: str, password: str) -> dict:
    if repositories.get_user_by_email(email) is not None:
        raise ValueError("Email already registered")
    return repositories.create_user(email, make_password(password))


def authenticate_user(email: str, password: str) -> dict | None:
    user = repositories.get_user_by_email(email)
    if user is None:
        return None
    if not check_password(password, user["password_hash"]):
        return None
    return user
