from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import check_password_hash

from operations.errors import BusinessRuleError


class LoginUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, email: str, password: str) -> dict | None:
        """Zwraca dane użytkownika, gdy e-mail i hasło są poprawne i konto jest aktywne.

        Zwraca None przy złym haśle, nieistniejącym e-mailu lub koncie
        zanonimizowanym. Przy poprawnym haśle do zablokowanego konta rzuca
        BusinessRuleError. Status sprawdzamy dopiero po haśle, żeby po samym
        e-mailu nie dało się ustalić, że konto jest zablokowane.
        Nigdy nie zwraca password_hash.
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
                  AND status IN ('Active', 'Blocked')
                LIMIT 1
            """),
            {"email": email},
        ).mappings().first()

        if row is None:
            return None

        if not check_password_hash(row["password_hash"], password):
            return None

        if row["status"] == "Blocked":
            raise BusinessRuleError(
                "Twoje konto zostało zablokowane. Skontaktuj się z administratorem portalu."
            )

        result = dict(row)
        result.pop("password_hash", None)
        return result
