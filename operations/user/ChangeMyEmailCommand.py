from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import check_password_hash

from operations.errors import BusinessRuleError, NotFoundError


class ChangeMyEmailCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int, *, email: str, current_password: str) -> None:
        """Zmiana własnego e-maila z „Mój profil”. Wymaga obecnego hasła."""
        row = self.connection.execute(
            text("""
                SELECT email, password_hash
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

        if email == row["email"]:
            raise BusinessRuleError("To jest Twój obecny adres e-mail.")

        taken = self.connection.execute(
            text("SELECT 1 FROM users WHERE email = :email AND id <> :id LIMIT 1"),
            {"email": email, "id": user_id},
        ).first()
        if taken is not None:
            raise BusinessRuleError("Konto z takim adresem e-mail już istnieje.")

        self.connection.execute(
            text("""
                UPDATE users
                SET
                    email = :email,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :id
            """),
            {"id": user_id, "email": email},
        )
