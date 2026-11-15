from sqlalchemy.engine import Connection

from operations.pagination import like_pattern, paginate


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
        conditions = []
        params: dict = {}

        search = search.strip()
        if search:
            conditions.append(
                "(email LIKE :search ESCAPE '\\'"
                " OR first_name LIKE :search ESCAPE '\\'"
                " OR last_name LIKE :search ESCAPE '\\')"
            )
            params["search"] = like_pattern(search)

        if status:
            conditions.append("status = :status")
            params["status"] = status

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        return paginate(
            self.connection,
            count_sql=f"SELECT COUNT(*) FROM users {where}",
            items_sql=f"""
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
            """,
            params=params,
            page=page,
            limit=limit,
        )
