from django.conf import settings

from . import repositories


def create_order(user_id, idempotency_key: str, items: list[dict]) -> dict:
    raise NotImplementedError


def get_order(order_id) -> dict:
    raise NotImplementedError


def cancel_order(order_id) -> dict:
    raise NotImplementedError
