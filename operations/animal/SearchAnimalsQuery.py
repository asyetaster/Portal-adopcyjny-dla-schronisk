from sqlalchemy.engine import Connection

from operations.common import (
    MAIN_PHOTO_ALT_SQL,
    MAIN_PHOTO_PATH_SQL,
    NEEDS_CONFIRMATION_SQL,
    VISIBLE_ANIMAL_SQL,
)
from operations.pagination import like_pattern, paginate

SORTS = {
    "published": "a.published_at DESC, a.id DESC",  # BR-019
    "confirmed": "a.last_confirmed_at DESC, a.id DESC",  # BR-019
}
NO_UPPER_AGE_LIMIT = 10_000


class SearchAnimalsQuery:
    """Publiczny katalog kart. Filtry działają łącznie (BR-016).

    - widoczność: ``VISIBLE_ANIMAL_SQL`` (nie szkic, nie ukryta, placówka zatwierdzona),
    - domyślnie tylko ``Available``; ``include_in_progress`` dodaje karty
      „w trakcie adopcji” (BR-020),
    - wiek: karta pasuje, gdy jej przedział ma część wspólną z podanym (BR-016);
      karta bez podanego wieku nie pasuje do filtra wieku,
    - ``sizes``: CSV, np. ``"Small,Medium"``; ``-1`` przy wieku = brak granicy.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        text: str = "",
        shelter_id: int = 0,
        species: str = "",
        sex: str = "",
        sizes: str = "",
        voivodeship: str = "",
        city: str = "",
        age_from_months: int = -1,
        age_to_months: int = -1,
        include_in_progress: bool = False,
        sort: str = "published",
        page: int = 1,
        limit: int = 12,
    ) -> dict:
        conditions = [VISIBLE_ANIMAL_SQL]
        params: dict = {}

        if include_in_progress:
            conditions.append("a.status IN ('Available', 'AdoptionInProgress')")
        else:
            conditions.append("a.status = 'Available'")

        if text.strip():
            conditions.append(
                "(a.name LIKE :text ESCAPE '\\' OR a.breed LIKE :text ESCAPE '\\')"
            )
            params["text"] = like_pattern(text.strip())
        if shelter_id > 0:
            conditions.append("a.shelter_id = :shelter_id")
            params["shelter_id"] = shelter_id
        if species:
            conditions.append("a.species = :species")
            params["species"] = species
        if sex:
            conditions.append("a.sex = :sex")
            params["sex"] = sex
        size_list = [s.strip() for s in sizes.split(",") if s.strip()]
        if size_list:
            names = []
            for i, size in enumerate(size_list):
                params[f"size{i}"] = size
                names.append(f":size{i}")
            conditions.append(f"a.size IN ({', '.join(names)})")
        if voivodeship:
            conditions.append("s.voivodeship = :voivodeship")
            params["voivodeship"] = voivodeship
        if city.strip():
            conditions.append("s.city LIKE :city ESCAPE '\\'")
            params["city"] = like_pattern(city.strip())
        if age_from_months >= 0 or age_to_months >= 0:
            conditions.append(
                "a.age_min_months IS NOT NULL "
                "AND a.age_min_months <= :age_to AND a.age_max_months >= :age_from"
            )
            params["age_from"] = max(age_from_months, 0)
            params["age_to"] = age_to_months if age_to_months >= 0 else NO_UPPER_AGE_LIMIT

        where = "WHERE " + " AND ".join(f"({c.strip()})" for c in conditions)
        return paginate(
            self.connection,
            count_sql=f"""
                SELECT COUNT(*) FROM animals a
                JOIN shelters s ON s.id = a.shelter_id {where}
            """,
            items_sql=f"""
                SELECT
                    a.id, a.name, a.species, a.sex, a.breed, a.size,
                    a.age_min_months, a.age_max_months, a.status,
                    a.published_at, a.last_confirmed_at,
                    {NEEDS_CONFIRMATION_SQL} AS needs_confirmation,
                    s.id AS shelter_id, s.name AS shelter_name,
                    s.city, s.voivodeship,
                    {MAIN_PHOTO_PATH_SQL} AS photo_path,
                    {MAIN_PHOTO_ALT_SQL} AS photo_alt
                FROM animals a
                JOIN shelters s ON s.id = a.shelter_id
                {where}
                ORDER BY {SORTS.get(sort, SORTS["published"])}
            """,
            params=params,
            page=page,
            limit=limit,
        )