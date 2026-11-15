from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetShelterForManagementQuery:
    """Panel placówki: pełne dane do formularza i dashboardu."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int) -> dict | None:
        row = self.connection.execute(
            text("""
                SELECT
                    s.*,
                    (SELECT COUNT(*) FROM shelter_employees e
                      WHERE e.shelter_id = s.id) AS employee_count,
                    (SELECT COUNT(*) FROM shelter_employees e
                      WHERE e.shelter_id = s.id AND e.is_manager = 1) AS manager_count
                FROM shelters s
                WHERE s.id = :id
            """),
            {"id": shelter_id},
        ).mappings().first()
        return dict(row) if row is not None else None
