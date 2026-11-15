from sqlalchemy.engine import Connection

from operations.pagination import like_pattern, paginate


class ListSheltersQuery:
    """Admin: wszystkie placówki, filtr po statusie i tekście (nazwa, miasto, e-mail)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        status: str = "",
        search: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        conditions = []
        params: dict = {}
        if status:
            conditions.append("status = :status")
            params["status"] = status
        if search.strip():
            conditions.append(
                "(name LIKE :search ESCAPE '\\'"
                " OR city LIKE :search ESCAPE '\\'"
                " OR contact_email LIKE :search ESCAPE '\\')"
            )
            params["search"] = like_pattern(search.strip())

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        return paginate(
            self.connection,
            count_sql=f"SELECT COUNT(*) FROM shelters {where}",
            items_sql=f"""
                SELECT id, name, city, voivodeship, contact_email, status,
                       submitted_at, decided_at
                FROM shelters
                {where}
                ORDER BY submitted_at DESC, id DESC
            """,
            params=params,
            page=page,
            limit=limit,
        )
