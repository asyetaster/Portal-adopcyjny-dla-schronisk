from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import generate_password_hash

from operations.errors import BusinessRuleError
from operations.user import MIN_PASSWORD_LENGTH


class RegisterUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: str = "",
    ) -> int:
        """Zakłada zwykłe konto (bez uprawnień administratora).

        Telefon jest opcjonalny (BR-050): pusty tekst zapisujemy jako NULL.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise BusinessRuleError(
                f"Hasło musi mieć co najmniej {MIN_PASSWORD_LENGTH} znaków."
            )

        exists = self.connection.execute(
            text("SELECT 1 FROM users WHERE email = :email LIMIT 1"),
            {"email": email},
        ).first()
        if exists is not None:
            raise BusinessRuleError("Konto z takim adresem e-mail już istnieje.")

        result = self.connection.execute(
            text("""
                INSERT INTO users (email, password_hash, first_name, last_name, phone)
                VALUES (:email, :password_hash, :first_name, :last_name, :phone)
            """),
            {
                "email": email,
                "password_hash": generate_password_hash(password),
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone or None,
            },
        )

        user_id = result.lastrowid
        if user_id is None:
            raise RuntimeError("Nie udało się odczytać ID użytkownika")

        return user_id
