from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import check_password_hash


class LoginUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, email: str, password: str) -> dict | None:
        """Zwraca dane użytkownika, gdy e-mail i hasło są poprawne i konto jest aktywne.

        Zwraca None przy złym haśle, nieistniejącym e-mailu lub koncie o statusie
        innym niż 'Active'. Nigdy nie zwraca password_hash.
        """
        row = self.connection.execute(
            text("""
                SELECT
                    id,
                    email,
                    first_name,
                    is_admin,
                    status,
                    password_hash
                FROM users
                WHERE email = :email
                  AND status = 'Active'
                LIMIT 1
            """),
            {"email": email},
        ).mappings().first()

        if row is None:
            return None

        if not check_password_hash(row["password_hash"], password):
            return None

        result = dict(row)
        result.pop("password_hash", None)
        return result
