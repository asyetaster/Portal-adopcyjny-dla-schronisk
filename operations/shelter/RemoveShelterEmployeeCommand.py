from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError
from operations.shelter import get_shelter_status


class RemoveShelterEmployeeCommand:
    """Kierownik usuwa pracownika. Nie można usunąć ostatniego kierownika (R1)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, user_id: int) -> None:
        if get_shelter_status(self.connection, shelter_id) == "Blocked":
            raise BusinessRuleError("Placówka jest zablokowana — panel działa tylko do odczytu.")

        is_manager = self.connection.execute(
            text("""
                SELECT is_manager FROM shelter_employees
                WHERE shelter_id = :shelter_id AND user_id = :user_id
            """),
            {"shelter_id": shelter_id, "user_id": user_id},
        ).scalar_one_or_none()
        if is_manager is None:
            raise NotFoundError()

        if is_manager:
            managers = self.connection.execute(
                text("""
                    SELECT COUNT(*) FROM shelter_employees
                    WHERE shelter_id = :shelter_id AND is_manager = 1
                """),
                {"shelter_id": shelter_id},
            ).scalar_one()
            if managers <= 1:
                raise BusinessRuleError("Nie można usunąć ostatniego kierownika placówki.")

        self.connection.execute(
            text("""
                DELETE FROM shelter_employees
                WHERE shelter_id = :shelter_id AND user_id = :user_id
            """),
            {"shelter_id": shelter_id, "user_id": user_id},
        )
