from sqlalchemy import text
from sqlalchemy.engine import Connection


class UpdateUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, user_id: int, new_name: str) -> int:
        result = self.connection.execute(
            text("UPDATE users SET name = :name WHERE id = :id"),
            {"id": user_id, "name": new_name},
        )
        return result.rowcount