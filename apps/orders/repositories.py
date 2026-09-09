from django.db import connection


def find_order_by_idempotency_key(key: str) -> dict | None:
    raise NotImplementedError


def create_order_with_items(user_id, idempotency_key: str, expires_at, items: list[dict]) -> dict:
    raise NotImplementedError


def get_order_with_items(order_id) -> dict | None:
    raise NotImplementedError


def cancel_order(order_id) -> bool:
    raise NotImplementedError


def find_expired_pending_order_ids() -> list:
    raise NotImplementedError
