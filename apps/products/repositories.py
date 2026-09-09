from django.db import connection


def _row_to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def create_product(name: str, price, stock_quantity: int) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO products (name, price, stock_quantity)
            VALUES (%s, %s, %s)
            RETURNING id, name, price, stock_quantity, created_at
            """,
            [name, price, stock_quantity],
        )
        row = cursor.fetchone()
        return _row_to_dict(cursor, row)


def get_product_by_id(product_id) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, price, stock_quantity, created_at
            FROM products
            WHERE id = %s
            """,
            [product_id],
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_dict(cursor, row)


def reserve_stock(product_id, quantity: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE id = %s AND stock_quantity >= %s
            RETURNING stock_quantity
            """,
            [quantity, product_id, quantity],
        )
        row = cursor.fetchone()
        return row is not None


def release_stock(product_id, quantity: int) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity + %s
            WHERE id = %s
            """,
            [quantity, product_id],
        )
