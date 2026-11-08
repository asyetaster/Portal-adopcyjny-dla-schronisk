from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import NotFoundError


class MakeAdminCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, email: str) -> None:
        """Nadaje uprawnienia administratora (R1).

        Tylko z konsoli: ``python test.py MakeAdminCommand --email ...``.
        """
        result = self.connection.execute(
            text("""
                UPDATE users
                SET
                    is_admin = 1,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE email = :email
            """),
            {"email": email},
        )

        if result.rowcount == 0:
            raise NotFoundError(f"Brak użytkownika {email}")
