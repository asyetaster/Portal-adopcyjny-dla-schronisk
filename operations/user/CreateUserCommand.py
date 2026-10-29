from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import generate_password_hash


class CreateUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: str | None = None,
        is_admin: bool = False,
    ) -> int:
        result = self.connection.execute(
            text("""
                INSERT INTO users (
                    email,
                    password_hash,
                    first_name,
                    last_name,
                    phone,
                    is_admin
                )
                VALUES (
                    :email,
                    :password_hash,
                    :first_name,
                    :last_name,
                    :phone,
                    :is_admin
                )
            """),
            {
                "email": email,
                "password_hash": generate_password_hash(password),
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "is_admin": int(is_admin),
            },
        )

        user_id = result.lastrowid
        if user_id is None:
            raise RuntimeError("Nie udało się odczytać ID użytkownika")

        return user_id