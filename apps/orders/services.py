"""Orders business logic."""

from django.conf import settings

from . import repositories


def create_order(user_id: int, idempotency_key: str, items: list[dict]) -> dict:
    """TODO:
    1. expires_at = now() + settings.ORDER_PENDING_TTL_MINUTES daqiqa
    2. repositories.create_order_with_items(...) chaqirish
    3. Agar stock yetmasa -> service-level exception (view 409/422 ga map qiladi)
    4. Muvaffaqiyatli natijani qaytarish
    """
    raise NotImplementedError


def get_order(order_id: int) -> dict:
    """TODO:
    1. Avval Redis cache'dan `order:{id}` o'qish (cache-aside)
    2. Topilmasa repositories.get_order_with_items, keyin cache'ga yozish (TTL ~60s)
    3. Topilmasa umuman -> 404 uchun exception
    """
    raise NotImplementedError


def cancel_order(order_id: int) -> dict:
    """TODO:
    1. repositories.cancel_order(order_id) chaqirish
    2. Agar False -> "already confirmed/cancelled" xatosi (409)
    3. Muvaffaqiyatli bo'lsa -> Redis'dan `order:{id}` keyni invalidatsiya qilish (DEL)
    4. Yangilangan order'ni qaytarish
    """
    raise NotImplementedError
