from sqlalchemy import text
from sqlalchemy.engine import Connection


class ListMySheltersQuery:
    """Placówki, w których użytkownik pracuje, ze statusem i powodem odrzucenia."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> list[dict]:
        rows = self.connection.execute(
            text("""
                SELECT
                    s.id,
                    s.name,
                    s.city,
                    s.voivodeship,
                    s.status,
                    s.rejection_reason,
                    s.blocked_reason,
                    s.submitted_at,
                    s.decided_at,
                    e.is_manager
                FROM shelter_employees e
                JOIN shelters s ON s.id = e.shelter_id
                WHERE e.user_id = :user_id
                ORDER BY s.name, s.id
            """),
            {"user_id": user_id},
        ).mappings().all()
        return [dict(row) for row in rows]
