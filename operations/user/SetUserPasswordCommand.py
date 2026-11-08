from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import generate_password_hash

from operations.errors import BusinessRuleError, NotFoundError
from operations.user import MIN_PASSWORD_LENGTH


class SetUserPasswordCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, email: str, password: str) -> None:
        """Ustawia nowe hasło (R2, zamiast odzyskiwania hasła).

        Tylko z konsoli: ``python test.py SetUserPasswordCommand --email ... --password ...``.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise BusinessRuleError(
                f"Hasło musi mieć co najmniej {MIN_PASSWORD_LENGTH} znaków."
            )

        result = self.connection.execute(
            text("""
                UPDATE users
                SET
                    password_hash = :password_hash,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE email = :email
            """),
            {"email": email, "password_hash": generate_password_hash(password)},
        )

        if result.rowcount == 0:
            raise NotFoundError(f"Brak użytkownika {email}")
