from sqlalchemy import text
from sqlalchemy.engine import Connection


class ListUsersQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, limit: int = 100, page: int = 1) -> list[dict]:
        offset = max((page - 1) * limit, 0)
        rows = self.connection.execute(
            text("SELECT id, name FROM users ORDER BY id LIMIT :offset, :limit"),
            {"limit": limit, "offset": offset},
        ).mappings().all()
        return [dict(row) for row in rows]