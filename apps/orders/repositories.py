import json

from django.db import connection

from apps.products import repositories as product_repositories


def _row_to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def claim_idempotency_key(user_id, idempotency_key: str):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO idempotency_keys (user_id, idempotency_key, status)
            VALUES (%s, %s, 'processing')
            ON CONFLICT (user_id, idempotency_key) DO NOTHING
            RETURNING id
            """,
            [user_id, idempotency_key],
        )
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None


def get_idempotency_record(user_id, idempotency_key: str) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, status, order_id, response_code, response_body
            FROM idempotency_keys
            WHERE user_id = %s AND idempotency_key = %s
            """,
            [user_id, idempotency_key],
        )
        row = cursor.fetchone()
        if row is None:
            return None
        record = _row_to_dict(cursor, row)
        if isinstance(record.get("response_body"), str):
            record["response_body"] = json.loads(record["response_body"])
        return record


def complete_idempotency_key(record_id, order_id, response_code: int, response_body: dict) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE idempotency_keys
            SET status = 'completed', order_id = %s, response_code = %s, response_body = %s
            WHERE id = %s
            """,
            [order_id, response_code, json.dumps(response_body), record_id],
        )


def create_order(user_id, expires_at) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO orders (user_id, status, total_price, expires_at)
            VALUES (%s, 'pending', 0, %s)
            RETURNING id, user_id, status, total_price, created_at, expires_at
            """,
            [user_id, expires_at],
        )
        row = cursor.fetchone()
        return _row_to_dict(cursor, row)


def add_order_item(order_id, product_id, quantity: int, unit_price) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            [order_id, product_id, quantity, unit_price],
        )


def set_order_total(order_id, total_price) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE orders SET total_price = %s WHERE id = %s",
            [total_price, order_id],
        )


def reserve_items_or_none(items: list[dict]) -> list[dict] | None:
    reserved = []
    for item in items:
        result = product_repositories.reserve_stock(item["product_id"], item["quantity"])
        if result is None:
            return None
        reserved.append(
            {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "unit_price": result["price"],
            }
        )
    return reserved


def get_order_with_items(order_id) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, user_id, status, total_price, created_at, expires_at,
                   confirmed_at, cancelled_at
            FROM orders
            WHERE id = %s
            """,
            [order_id],
        )
        row = cursor.fetchone()
        if row is None:
            return None
        order = _row_to_dict(cursor, row)

        cursor.execute(
            """
            SELECT id, product_id, quantity, unit_price
            FROM order_items
            WHERE order_id = %s
            """,
            [order_id],
        )
        columns = [col[0] for col in cursor.description]
        order["items"] = [dict(zip(columns, r)) for r in cursor.fetchall()]

    return order


def cancel_order(order_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT status FROM orders WHERE id = %s FOR UPDATE",
            [order_id],
        )
        row = cursor.fetchone()
        if row is None or row[0] != "pending":
            return False

        cursor.execute(
            """
            UPDATE orders
            SET status = 'cancelled', cancelled_at = now()
            WHERE id = %s
            """,
            [order_id],
        )

        cursor.execute(
            "SELECT product_id, quantity FROM order_items WHERE order_id = %s",
            [order_id],
        )
        items = cursor.fetchall()

    for product_id, quantity in items:
        product_repositories.release_stock(product_id, quantity)

    return True


def confirm_order(order_id) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT status FROM orders WHERE id = %s FOR UPDATE",
            [order_id],
        )
        row = cursor.fetchone()
        if row is None or row[0] != "pending":
            return False

        cursor.execute(
            """
            UPDATE orders
            SET status = 'confirmed', confirmed_at = now()
            WHERE id = %s
            """,
            [order_id],
        )

    return True


def find_expired_pending_order_ids() -> list:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id FROM orders
            WHERE status = 'pending' AND expires_at < now()
            """
        )
        return [row[0] for row in cursor.fetchall()]
