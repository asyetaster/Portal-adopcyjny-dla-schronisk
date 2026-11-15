from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetCurrentUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> dict | None:
        """Zwraca minimalny zestaw danych użytkownika do autoryzacji (g.user).

        Pola: id, first_name, is_admin, status oraz ``shelters`` — lista placówek,
        w których użytkownik pracuje (id, name, status, is_manager).
        None, gdy użytkownik nie istnieje.
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

        if row is None:
            return None

        shelters = self.connection.execute(
            text("""
                SELECT
                    s.id,
                    s.name,
                    s.status,
                    e.is_manager
                FROM shelter_employees e
                JOIN shelters s ON s.id = e.shelter_id
                WHERE e.user_id = :id
                ORDER BY s.name, s.id
            """),
            {"id": user_id},
        ).mappings().all()

        return {**dict(row), "shelters": [dict(s) for s in shelters]}
