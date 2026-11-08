from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetMyProfileQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> dict | None:
        """Dane do strony „Mój profil”. None, gdy użytkownik nie istnieje."""
        row = self.connection.execute(
            text("""
                SELECT
                    id,
                    email,
                    first_name,
                    last_name,
                    phone,
                    created_at
                FROM users
                WHERE id = :id
                LIMIT 1
            """),
            {"id": user_id},
        ).mappings().first()

        return dict(row) if row is not None else None
