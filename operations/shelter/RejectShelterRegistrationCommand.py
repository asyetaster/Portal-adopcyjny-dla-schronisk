from sqlalchemy import text
from sqlalchemy.engine import Connection

from mailer import queue_mail
from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status
from operations.shelter.ApproveShelterRegistrationCommand import _submitter


class RejectShelterRegistrationCommand:
    """Admin: Pending → Rejected z powodem + mail do zgłaszającego."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, reason: str) -> None:
        reason = reason.strip()
        if not reason:
            raise BusinessRuleError("Podaj powód odrzucenia.")
        if get_shelter_status(self.connection, shelter_id) != "Pending":
            raise BusinessRuleError("Odrzucić można tylko zgłoszenie oczekujące.")

        self.connection.execute(
            text("""
                UPDATE shelters
                SET
                    status = 'Rejected',
                    decided_by = :actor_id,
                    decided_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    rejection_reason = :reason,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {"shelter_id": shelter_id, "actor_id": actor_id, "reason": reason},
        )

        submitter = _submitter(self.connection, shelter_id)
        queue_mail(
            submitter["email"],
            f"Placówka „{submitter['shelter_name']}” została odrzucona",
            "shelter_rejected.txt",
            first_name=submitter["first_name"],
            shelter_name=submitter["shelter_name"],
            reason=reason,
        )
