from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetCurrentUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> dict | None:
        """Zwraca minimalny zestaw danych użytkownika do autoryzacji (g.user).

        Pola: id, first_name, is_admin, status. None, gdy użytkownik nie istnieje.
        Lista placówek (shelters) pojawi się w M2 — na razie pomijamy.
        """
        row = self.connection.execute(
            text("""
                SELECT
                    id,
                    first_name,
                    is_admin,
                    status
                FROM users
                WHERE id = :id
                LIMIT 1
            """),
            {"id": user_id},
        ).mappings().first()

        return dict(row) if row is not None else None
