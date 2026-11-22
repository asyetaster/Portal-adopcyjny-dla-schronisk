from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.common import NEEDS_CONFIRMATION_SQL, VISIBLE_ANIMAL_SQL


class GetAnimalProfileQuery:
    """Publiczna karta zwierzęcia; ``None``, gdy karta nie jest widoczna (BR-012, R6).

    ``viewer_id`` (zalogowany użytkownik albo 0) zostaje w sygnaturze pod M4,
    gdzie posłuży do ``is_favorite``. Wynik nie zawiera żadnych danych osobowych.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, animal_id: int, viewer_id: int = 0) -> dict | None:
        row = self.connection.execute(
            text(f"""
                SELECT
                    a.id, a.name, a.species, a.sex, a.breed, a.size,
                    a.age_min_months, a.age_max_months, a.description,
                    a.daily_needs, a.temperament, a.status, a.published_at,
                    a.last_confirmed_at, a.donations_enabled,
                    {NEEDS_CONFIRMATION_SQL} AS needs_confirmation,
                    s.id AS shelter_id, s.name AS shelter_name, s.city, s.voivodeship,
                    s.street_address, s.postal_code, s.contact_email, s.contact_phone
                FROM animals a
                JOIN shelters s ON s.id = a.shelter_id
                WHERE a.id = :id AND {VISIBLE_ANIMAL_SQL}
            """),
            {"id": animal_id},
        ).mappings().first()
        if row is None:
            return None
        animal = dict(row)

        photos = self.connection.execute(
            text("""
                SELECT id, file_path, alt_text, is_main FROM animal_photos
                WHERE animal_id = :id ORDER BY is_main DESC, position, id
            """),
            {"id": animal_id},
        ).mappings().all()
        requirements = self.connection.execute(
            text("""
                SELECT good_with_children, good_with_dogs, good_with_cats,
                       activity_level, min_experience, special_care_required,
                       special_care_notes, notes_to_discuss
                FROM animal_care_requirements WHERE animal_id = :id
            """),
            {"id": animal_id},
        ).mappings().first()

        animal["photos"] = [dict(p) for p in photos]
        animal["requirements"] = dict(requirements) if requirements else None
        animal["temperament_tags"] = (
            animal["temperament"].split(",") if animal["temperament"] else []
        )
        return animal