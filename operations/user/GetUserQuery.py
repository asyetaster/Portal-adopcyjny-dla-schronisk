from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetUserQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int) -> dict | None:
        row = self.connection.execute(
            text("SELECT id, name FROM users WHERE id = :id LIMIT 1"),
            {"id": user_id},
        ).mappings().first()
        return dict(row) if row is not None else None