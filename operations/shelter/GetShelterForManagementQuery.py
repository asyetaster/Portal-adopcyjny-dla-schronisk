from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.common import NEEDS_CONFIRMATION_SQL

class GetShelterForManagementQuery:
    """Panel placówki: pełne dane do formularza i dashboardu."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int) -> dict | None:
        row = self.connection.execute(
            text(f"""
                SELECT
                    s.*,
                    (SELECT COUNT(*) FROM shelter_employees e
                      WHERE e.shelter_id = s.id) AS employee_count,
                    (SELECT COUNT(*) FROM shelter_employees e
                      WHERE e.shelter_id = s.id AND e.is_manager = 1) AS manager_count,
                    (SELECT COUNT(*) FROM animals a
                      WHERE a.shelter_id = s.id) AS animal_count,
                    (SELECT COUNT(*) FROM animals a
                      WHERE a.shelter_id = s.id AND a.status = 'Available') AS available_animal_count,
                    (SELECT COUNT(*) FROM animals a
                      WHERE a.shelter_id = s.id AND ({NEEDS_CONFIRMATION_SQL}) = 1) AS needs_confirmation_count
                FROM shelters s
                WHERE s.id = :id
            """),
            {"id": shelter_id},
        ).mappings().first()
        return dict(row) if row is not None else None
