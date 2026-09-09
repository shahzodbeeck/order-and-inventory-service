"""Orders uchun raw SQL repository qatlami. Faqat SQL, ORM query yo'q."""

from django.db import connection


def find_order_by_idempotency_key(key: str) -> dict | None:
    """TODO:
    SELECT id, status, ... FROM orders WHERE idempotency_key = %s;

    Variant: INSERT ... ON CONFLICT (idempotency_key) DO NOTHING RETURNING *
    yondashuvi ishlatilsa, bu funksiya alohida kerak bo'lmasligi mumkin —
    create_order_with_items ichida hal qilinadi.
    """
    raise NotImplementedError


def create_order_with_items(user_id: int, idempotency_key: str, expires_at, items: list[dict]) -> dict:
    """Bitta transaction ichida:

    TODO:
    1. BEGIN (Django: transaction.atomic())
    2. INSERT INTO orders (...) VALUES (...) ON CONFLICT (idempotency_key) DO NOTHING RETURNING id
       - agar conflict bo'lsa (id qaytmasa) -> mavjud orderni idempotency_key bo'yicha
         qayta o'qib qaytarish, items yaratmaslik, stock kamaytirmaslik
    3. Har bir item uchun products.repositories.reserve_stock(product_id, qty) chaqirish
       - agar biror item False qaytarsa -> transaction rollback, "insufficient stock" xato
    4. INSERT INTO order_items (...) har bir item uchun
    5. COMMIT
    """
    raise NotImplementedError


def get_order_with_items(order_id: int) -> dict | None:
    """TODO:
    SELECT orders.* FROM orders WHERE id = %s;
    SELECT * FROM order_items WHERE order_id = %s;
    ikkisini birlashtirib dict qaytarish.
    """
    raise NotImplementedError


def cancel_order(order_id: int) -> bool:
    """TODO (bitta transactionda):
    1. SELECT status FROM orders WHERE id = %s FOR UPDATE;
    2. agar status != 'pending' -> False qaytarish (allaqachon confirmed/cancelled)
    3. UPDATE orders SET status = 'cancelled' WHERE id = %s;
    4. har bir order_item uchun products.repositories.release_stock(product_id, qty)
    5. COMMIT -> True
    """
    raise NotImplementedError


def find_expired_pending_order_ids() -> list[int]:
    """Celery beat job uchun.

    TODO:
    SELECT id FROM orders WHERE status = 'pending' AND expires_at < now();
    """
    raise NotImplementedError
