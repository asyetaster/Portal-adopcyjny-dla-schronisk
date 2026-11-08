from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError


class UnblockUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, user_id: int) -> None:
        """Przywraca zablokowane konto do statusu 'Active'.

        ``actor_id`` zostaje w sygnaturze na potrzeby przyszłego dziennika zmian.
        """
        status = self.connection.execute(
            text("SELECT status FROM users WHERE id = :id"),
            {"id": user_id},
        ).scalar_one_or_none()

        if status is None:
            raise NotFoundError()
        if status != "Blocked":
            raise BusinessRuleError("To konto nie jest zablokowane.")

        self.connection.execute(
            text("""
                UPDATE users
                SET
                    status = 'Active',
                    blocked_reason = NULL,
                    blocked_at = NULL,
                    blocked_by = NULL,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :id
            """),
            {"id": user_id},
        )
