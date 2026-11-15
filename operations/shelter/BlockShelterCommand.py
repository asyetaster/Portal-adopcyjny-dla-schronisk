from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status


class BlockShelterCommand:
    """Admin: blokada placówki z powodem. Zmienia tylko ``shelters`` (D13, R5)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, reason: str) -> None:
        reason = reason.strip()
        if not reason:
            raise BusinessRuleError("Podaj powód blokady.")
        if get_shelter_status(self.connection, shelter_id) == "Blocked":
            raise BusinessRuleError("Placówka jest już zablokowana.")

        self.connection.execute(
            text("""
                UPDATE shelters
                SET
                    status = 'Blocked',
                    blocked_reason = :reason,
                    blocked_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    blocked_by = :actor_id,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {"shelter_id": shelter_id, "reason": reason, "actor_id": actor_id},
        )
