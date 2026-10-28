from sqlalchemy import text
from sqlalchemy.engine import Connection


class CreateUserCommand:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, name: str) -> int:
        result = self.connection.execute(
            text("INSERT INTO users (name) VALUES (:name)"),
            {"name": name},
        )
        return result.lastrowid