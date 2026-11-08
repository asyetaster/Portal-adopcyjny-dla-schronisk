from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import NotFoundError


class UpdateMyProfileCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        user_id: int,
        *,
        first_name: str,
        last_name: str,
        phone: str = "",
    ) -> None:
        """Zmienia imię, nazwisko i telefon. E-maila i hasła nie zmienia."""
        result = self.connection.execute(
            text("""
                UPDATE users
                SET
                    first_name = :first_name,
                    last_name = :last_name,
                    phone = :phone,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :id
                  AND status = 'Active'
            """),
            {
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone or None,
            },
        )

        if result.rowcount == 0:
            raise NotFoundError()
