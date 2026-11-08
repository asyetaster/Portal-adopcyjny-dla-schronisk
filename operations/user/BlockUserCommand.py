from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError


class BlockUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, user_id: int, reason: str) -> None:
        """Blokuje aktywne konto (BR-048: powód jest wymagany).

        Na razie zmienia tylko ``users``. Zamykanie zgłoszeń użytkownika (R4)
        dochodzi w M5, M6 i M7.
        """
        reason = reason.strip()
        if not reason:
            raise BusinessRuleError("Podaj powód blokady.")

        if actor_id == user_id:
            raise BusinessRuleError("Nie możesz zablokować własnego konta.")

        status = self.connection.execute(
            text("SELECT status FROM users WHERE id = :id"),
            {"id": user_id},
        ).scalar_one_or_none()

        if status is None:
            raise NotFoundError()
        if status != "Active":
            raise BusinessRuleError("Można zablokować tylko aktywne konto.")

        self.connection.execute(
            text("""
                UPDATE users
                SET
                    status = 'Blocked',
                    blocked_reason = :reason,
                    blocked_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    blocked_by = :actor_id,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :id
            """),
            {"id": user_id, "reason": reason, "actor_id": actor_id},
        )
