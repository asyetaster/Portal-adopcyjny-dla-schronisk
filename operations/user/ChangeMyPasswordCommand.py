from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import check_password_hash, generate_password_hash

from operations.errors import BusinessRuleError, NotFoundError
from operations.user import MIN_PASSWORD_LENGTH


class ChangeMyPasswordCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        user_id: int,
        *,
        current_password: str,
        new_password: str,
    ) -> None:
        """Zmiana własnego hasła z „Mój profil”. Wymaga obecnego hasła."""
        row = self.connection.execute(
            text("""
                SELECT password_hash
                FROM users
                WHERE id = :id
                  AND status = 'Active'
                LIMIT 1
            """),
            {"id": user_id},
        ).mappings().first()

        if row is None:
            raise NotFoundError()

        if not check_password_hash(row["password_hash"], current_password):
            raise BusinessRuleError("Niepoprawne obecne hasło.")

        if len(new_password) < MIN_PASSWORD_LENGTH:
            raise BusinessRuleError(
                f"Hasło musi mieć co najmniej {MIN_PASSWORD_LENGTH} znaków."
            )

        self.connection.execute(
            text("""
                UPDATE users
                SET
                    password_hash = :password_hash,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :id
            """),
            {"id": user_id, "password_hash": generate_password_hash(new_password)},
        )
