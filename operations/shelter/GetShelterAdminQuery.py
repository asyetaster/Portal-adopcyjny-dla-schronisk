from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetShelterAdminQuery:
    """Admin: szczegóły placówki ze zgłaszającym i listą pracowników."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int) -> dict | None:
        row = self.connection.execute(
            text("""
                SELECT
                    s.*,
                    u.first_name AS submitter_first_name,
                    u.last_name AS submitter_last_name,
                    u.email AS submitter_email
                FROM shelters s
                JOIN users u ON u.id = s.submitted_by
                WHERE s.id = :id
            """),
            {"id": shelter_id},
        ).mappings().first()
        if row is None:
            return None

        employees = self.connection.execute(
            text("""
                SELECT u.id, u.first_name, u.last_name, u.email, u.status,
                       e.is_manager, e.assigned_at
                FROM shelter_employees e
                JOIN users u ON u.id = e.user_id
                WHERE e.shelter_id = :id
                ORDER BY e.is_manager DESC, u.last_name, u.first_name
            """),
            {"id": shelter_id},
        ).mappings().all()

        return {**dict(row), "employees": [dict(e) for e in employees]}
