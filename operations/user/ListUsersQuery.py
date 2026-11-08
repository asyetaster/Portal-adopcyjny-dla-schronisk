from sqlalchemy import text
from sqlalchemy.engine import Connection


class ListUsersQuery:
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        search: str = "",
        status: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        """Lista kont dla administratora.

        ``search`` szuka w e-mailu, imieniu i nazwisku; ``status`` filtruje po
        statusie ('Active', 'Blocked', 'Anonymized'). Puste = bez filtra.
        """
        if limit < 1 or page < 1:
            raise ValueError("limit i page muszą być większe od 0")

        conditions = []
        params: dict = {}

        search = search.strip()
        if search:
            conditions.append(
                "(email LIKE :search ESCAPE '\\'"
                " OR first_name LIKE :search ESCAPE '\\'"
                " OR last_name LIKE :search ESCAPE '\\')"
            )
            escaped = (
                search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            )
            params["search"] = f"%{escaped}%"

        if status:
            conditions.append("status = :status")
            params["status"] = status

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        total = self.connection.execute(
            text(f"SELECT COUNT(*) FROM users {where}"),
            params,
        ).scalar_one()

        rows = self.connection.execute(
            text(f"""
                SELECT
                    id,
                    email,
                    first_name,
                    last_name,
                    phone,
                    is_admin,
                    status,
                    created_at,
                    updated_at
                FROM users
                {where}
                ORDER BY created_at DESC, id DESC
                LIMIT :limit OFFSET :offset
            """),
            {**params, "limit": limit, "offset": (page - 1) * limit},
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
