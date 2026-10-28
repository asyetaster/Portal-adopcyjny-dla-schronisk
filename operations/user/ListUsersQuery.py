from sqlalchemy import text
from sqlalchemy.engine import Connection


class ListUsersQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, limit: int = 20, page: int = 1) -> dict:
        if limit < 1 or page < 1:
            raise ValueError("limit i page muszą być większe od 0")

        offset = (page - 1) * limit

        total = self.connection.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar_one()

        rows = self.connection.execute(
            text("""
                SELECT id, name
                FROM users
                ORDER BY id
                LIMIT :limit OFFSET :offset
            """),
            {"limit": limit, "offset": offset},
        ).mappings().all()


        total_pages = (total + limit - 1) // limit

        return {
            "items": [dict(row) for row in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
        }