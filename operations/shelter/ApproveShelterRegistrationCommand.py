from sqlalchemy import text
from sqlalchemy.engine import Connection

from mailer import queue_mail
from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status


class ApproveShelterRegistrationCommand:
    """Admin: Pending → Approved + mail do zgłaszającego."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int) -> None:
        if get_shelter_status(self.connection, shelter_id) != "Pending":
            raise BusinessRuleError("Zatwierdzić można tylko zgłoszenie oczekujące.")

        self.connection.execute(
            text("""
                UPDATE shelters
                SET
                    status = 'Approved',
                    decided_by = :actor_id,
                    decided_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    rejection_reason = NULL,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {"shelter_id": shelter_id, "actor_id": actor_id},
        )

        submitter = _submitter(self.connection, shelter_id)
        queue_mail(
            submitter["email"],
            f"Placówka „{submitter['shelter_name']}” została zatwierdzona",
            "shelter_approved.txt",
            first_name=submitter["first_name"],
            shelter_name=submitter["shelter_name"],
        )


def _submitter(connection: Connection, shelter_id: int) -> dict:
    return dict(
        connection.execute(
            text("""
                SELECT u.email, u.first_name, s.name AS shelter_name
                FROM shelters s
                JOIN users u ON u.id = s.submitted_by
                WHERE s.id = :id
            """),
            {"id": shelter_id},
        ).mappings().one()
    )
