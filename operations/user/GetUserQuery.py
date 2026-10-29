from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> dict | None:
        row = self.connection.execute(
            text("""
                SELECT
                    id,
                    email,
                    first_name,
                    last_name,
                    phone,
                    is_admin,
                    status,
                    blocked_reason,
                    blocked_at,
                    blocked_by,
                    anonymized_at,
                    created_at,
                    updated_at
                FROM users
                WHERE id = :id
                LIMIT 1
            """),
            {"id": user_id},
        ).mappings().first()

        return dict(row) if row is not None else None