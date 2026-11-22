from sqlalchemy.engine import Connection

from operations.common import MAIN_PHOTO_PATH_SQL
from operations.pagination import like_pattern, paginate


class ListAnimalsForModerationQuery:
    """Admin: karty ze wszystkich placówek (także szkice), do ukrywania i przywracania."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        search: str = "",
        hidden_only: bool = False,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        conditions = []
        params: dict = {}
        if search.strip():
            conditions.append(
                "(a.name LIKE :search ESCAPE '\\' OR s.name LIKE :search ESCAPE '\\')"
            )
            params["search"] = like_pattern(search.strip())
        if hidden_only:
            conditions.append("a.is_hidden = 1")

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        return paginate(
            self.connection,
            count_sql=f"""
                SELECT COUNT(*) FROM animals a
                JOIN shelters s ON s.id = a.shelter_id {where}
            """,
            items_sql=f"""
                SELECT
                    a.id, a.name, a.species, a.status, a.is_hidden, a.hidden_reason,
                    a.hidden_at, a.published_at, a.shelter_id,
                    s.name AS shelter_name, s.status AS shelter_status,
                    {MAIN_PHOTO_PATH_SQL} AS photo_path
                FROM animals a
                JOIN shelters s ON s.id = a.shelter_id
                {where}
                ORDER BY a.is_hidden DESC, a.updated_at DESC, a.id DESC
            """,
            params=params,
            page=page,
            limit=limit,
        )