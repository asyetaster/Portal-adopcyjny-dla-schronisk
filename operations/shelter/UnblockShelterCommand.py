from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status


class UnblockShelterCommand:
    """Admin: odblokowanie. Approved, gdy placówka była zatwierdzona, w przeciwnym razie Pending."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int) -> None:
        if get_shelter_status(self.connection, shelter_id) != "Blocked":
            raise BusinessRuleError("Placówka nie jest zablokowana.")

        # decided_at bez rejection_reason = była zatwierdzona. Odrzucona i potem
        # zablokowana wraca do Rejected, żeby zachować powód odrzucenia.
        self.connection.execute(
            text("""
                UPDATE shelters
                SET
                    status = CASE
                        WHEN decided_at IS NULL THEN 'Pending'
                        WHEN rejection_reason IS NOT NULL THEN 'Rejected'
                        ELSE 'Approved'
                    END,
                    blocked_reason = NULL,
                    blocked_at = NULL,
                    blocked_by = NULL,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {"shelter_id": shelter_id},
        )
