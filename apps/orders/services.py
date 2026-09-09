from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from . import repositories

ORDER_CACHE_TTL_SECONDS = 60


class InsufficientStockError(Exception):
    pass


class IdempotencyInProgressError(Exception):
    pass


class OrderNotCancellableError(Exception):
    pass


class OrderNotConfirmableError(Exception):
    pass


def _order_cache_key(order_id) -> str:
    return f"order:{order_id}"


def _serialize_order(order: dict) -> dict:
    return {
        "id": str(order["id"]),
        "status": order["status"],
        "total_price": str(order["total_price"]),
        "created_at": order["created_at"].isoformat(),
        "expires_at": order["expires_at"].isoformat() if order["expires_at"] else None,
        "items": [
            {
                "product_id": str(item["product_id"]),
                "quantity": item["quantity"],
                "unit_price": str(item["unit_price"]),
            }
            for item in order.get("items", [])
        ],
    }


@transaction.atomic
def create_order(user_id, idempotency_key: str, items: list[dict]) -> dict:
    claimed_id = repositories.claim_idempotency_key(user_id, idempotency_key)

    if claimed_id is None:
        record = repositories.get_idempotency_record(user_id, idempotency_key)
        if record["status"] == "completed":
            return {
                "replayed": True,
                "response_code": record["response_code"],
                "body": record["response_body"],
            }
        raise IdempotencyInProgressError

    reserved_items = repositories.reserve_items_or_none(items)
    if reserved_items is None:
        raise InsufficientStockError

    expires_at = timezone.now() + timedelta(minutes=settings.ORDER_PENDING_TTL_MINUTES)
    order = repositories.create_order(user_id, expires_at)

    total_price = 0
    for item in reserved_items:
        repositories.add_order_item(
            order["id"], item["product_id"], item["quantity"], item["unit_price"]
        )
        total_price += item["unit_price"] * item["quantity"]

    repositories.set_order_total(order["id"], total_price)

    order = repositories.get_order_with_items(order["id"])
    response_body = _serialize_order(order)

    repositories.complete_idempotency_key(claimed_id, order["id"], 201, response_body)

    return {"replayed": False, "response_code": 201, "body": response_body}


def get_order(order_id) -> dict:
    cache_key = _order_cache_key(order_id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    order = repositories.get_order_with_items(order_id)
    if order is None:
        return None

    serialized = _serialize_order(order)
    cache.set(cache_key, serialized, ORDER_CACHE_TTL_SECONDS)
    return serialized


def cancel_order(order_id) -> dict:
    cancelled = repositories.cancel_order(order_id)
    if not cancelled:
        raise OrderNotCancellableError

    cache.delete(_order_cache_key(order_id))

    order = repositories.get_order_with_items(order_id)
    return _serialize_order(order)


def confirm_order(order_id) -> dict:
    confirmed = repositories.confirm_order(order_id)
    if not confirmed:
        raise OrderNotConfirmableError

    cache.delete(_order_cache_key(order_id))

    order = repositories.get_order_with_items(order_id)
    return _serialize_order(order)
