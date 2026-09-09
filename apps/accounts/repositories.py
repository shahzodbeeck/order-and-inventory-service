from django.db import connection


def _row_to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def create_user(email: str, password_hash: str) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id, email, created_at
            """,
            [email, password_hash],
        )
        row = cursor.fetchone()
        return _row_to_dict(cursor, row)


def get_user_by_email(email: str) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, password_hash, created_at
            FROM users
            WHERE email = %s
            """,
            [email],
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_dict(cursor, row)


def get_user_by_id(user_id) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, created_at
            FROM users
            WHERE id = %s
            """,
            [user_id],
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_dict(cursor, row)
