from sqlalchemy.engine import Connection

from operations.common import MAIN_PHOTO_PATH_SQL, NEEDS_CONFIRMATION_SQL
from operations.pagination import like_pattern, paginate

SORTS = {
    "updated": "a.updated_at DESC, a.id DESC",
    "name": "a.name COLLATE NOCASE, a.id",
    # Najdawniej potwierdzone na górze: tym kartom trzeba się przyjrzeć najpierw.
    "confirmed": "a.last_confirmed_at IS NULL, a.last_confirmed_at, a.id",
}


class ListShelterAnimalsQuery:
    """Panel: karty placówki, także szkice, wycofane i adoptowane."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        shelter_id: int,
        text: str = "",
        status: str = "",
        species: str = "",
        sort: str = "updated",
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        conditions = ["a.shelter_id = :shelter_id"]
        params: dict = {"shelter_id": shelter_id}
        if text.strip():
            conditions.append("(a.name LIKE :text ESCAPE '\\' OR a.breed LIKE :text ESCAPE '\\')")
            params["text"] = like_pattern(text.strip())
        if status:
            conditions.append("a.status = :status")
            params["status"] = status
        if species:
            conditions.append("a.species = :species")
            params["species"] = species

        where = "WHERE " + " AND ".join(conditions)
        return paginate(
            self.connection,
            count_sql=f"SELECT COUNT(*) FROM animals a {where}",
            items_sql=f"""
                SELECT
                    a.id, a.name, a.species, a.sex, a.breed, a.size,
                    a.age_min_months, a.age_max_months,
                    a.status, a.is_hidden, a.updated_at, a.last_confirmed_at,
                    {NEEDS_CONFIRMATION_SQL} AS needs_confirmation,
                    {MAIN_PHOTO_PATH_SQL} AS photo_path
                FROM animals a
                {where}
                ORDER BY {SORTS.get(sort, SORTS["updated"])}
            """,
            params=params,
            page=page,
            limit=limit,
        )