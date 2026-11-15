from sqlalchemy.engine import Connection

from operations.pagination import like_pattern, paginate


class SearchSheltersQuery:
    """Publiczny katalog: tylko zatwierdzone placówki (BR-014)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        name: str = "",
        voivodeship: str = "",
        city: str = "",
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        conditions = ["status = 'Approved'"]
        params: dict = {}

        if name.strip():
            conditions.append("name LIKE :name ESCAPE '\\'")
            params["name"] = like_pattern(name.strip())
        if voivodeship.strip():
            conditions.append("voivodeship = :voivodeship")
            params["voivodeship"] = voivodeship.strip()
        if city.strip():
            conditions.append("city LIKE :city ESCAPE '\\'")
            params["city"] = like_pattern(city.strip())

        where = "WHERE " + " AND ".join(conditions)
        return paginate(
            self.connection,
            count_sql=f"SELECT COUNT(*) FROM shelters {where}",
            rows_sql=f"""
                SELECT id, name, description, city, voivodeship, website
                FROM shelters
                {where}
                ORDER BY name, id
                LIMIT :limit OFFSET :offset
            """,
            params=params,
            page=page,
            limit=limit,
        )
