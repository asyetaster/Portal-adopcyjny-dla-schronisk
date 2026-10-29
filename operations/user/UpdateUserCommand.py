from sqlalchemy import text
from sqlalchemy.engine import Connection
from werkzeug.security import generate_password_hash


class UpdateUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        user_id: int,
        *,
        email: str,
        first_name: str,
        last_name: str,
        phone: str | None = None,
        is_admin: bool = False,
        password: str | None = None,
    ) -> int:
        params = {
            "id": user_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "is_admin": int(is_admin),
        }

        password_assignment = ""
        if password is not None:
            params["password_hash"] = generate_password_hash(password)
            password_assignment = ", password_hash = :password_hash"

        result = self.connection.execute(
            text(f"""
                UPDATE users
                SET
                    email = :email,
                    first_name = :first_name,
                    last_name = :last_name,
                    phone = :phone,
                    is_admin = :is_admin,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                    {password_assignment}
                WHERE id = :id
            """),
            params,
        )

        return result.rowcount