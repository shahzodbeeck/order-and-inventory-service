"""Products uchun raw SQL repository qatlami.

Qoida: bu faylda faqat SQL va cursor ishlatiladi, hech qanday
Django ORM query (Model.objects...) ishlatilmaydi.
django.db.connection.cursor() dan foydalaning.
"""

from django.db import connection


def create_product(name: str, price, stock_quantity: int) -> dict:
    """TODO:
    INSERT INTO products (name, price, stock_quantity)
    VALUES (%s, %s, %s)
    RETURNING id, name, price, stock_quantity, created_at;
    """
    raise NotImplementedError


def get_product_by_id(product_id: int) -> dict | None:
    """TODO:
    SELECT id, name, price, stock_quantity, created_at
    FROM products WHERE id = %s;
    """
    raise NotImplementedError


def reserve_stock(product_id: int, quantity: int) -> bool:
    """Concurrency-safe stock kamaytirish.

    TODO (tavsiya etilgan variant — conditional atomic UPDATE, lock kerak emas):
    UPDATE products
    SET stock_quantity = stock_quantity - %s
    WHERE id = %s AND stock_quantity >= %s
    RETURNING stock_quantity;

    Agar RETURNING natija bo'sh bo'lsa (0 rows) -> False qaytaring
    (stock yetarli emas). Bu funksiya create_order xizmati ichida
    bitta transaction ostida, har bir order item uchun chaqiriladi.
    """
    raise NotImplementedError


def release_stock(product_id: int, quantity: int) -> None:
    """Cancel bo'lganda stock qaytarish.

    TODO:
    UPDATE products SET stock_quantity = stock_quantity + %s WHERE id = %s;
    """
    raise NotImplementedError
