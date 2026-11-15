from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status


class AssignShelterEmployeeCommand:
    """Kierownik dodaje pracownika po e-mailu. Konto musi być aktywne."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
        email: str,
        is_manager: bool = False,
    ) -> int:
        if get_shelter_status(self.connection, shelter_id) == "Blocked":
            raise BusinessRuleError("Placówka jest zablokowana — panel działa tylko do odczytu.")

        user = self.connection.execute(
            text("SELECT id, status FROM users WHERE email = :email"),
            {"email": email.strip()},
        ).mappings().first()
        if user is None or user["status"] != "Active":
            raise BusinessRuleError("Nie znaleziono aktywnego konta o tym adresie e-mail.")

        exists = self.connection.execute(
            text("""
                SELECT 1 FROM shelter_employees
                WHERE shelter_id = :shelter_id AND user_id = :user_id
            """),
            {"shelter_id": shelter_id, "user_id": user["id"]},
        ).first()
        if exists:
            raise BusinessRuleError("Ta osoba już pracuje w tej placówce.")

        self.connection.execute(
            text("""
                INSERT INTO shelter_employees (shelter_id, user_id, is_manager, assigned_by)
                VALUES (:shelter_id, :user_id, :is_manager, :actor_id)
            """),
            {
                "shelter_id": shelter_id,
                "user_id": user["id"],
                "is_manager": int(is_manager),
                "actor_id": actor_id,
            },
        )
        return user["id"]
