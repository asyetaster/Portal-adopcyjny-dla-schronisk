from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import count_photos, missing_for_publication
from operations.common import NEEDS_CONFIRMATION_SQL


class GetAnimalProfileForManagementQuery:
    """Panel: pełne dane karty (także szkic), zdjęcia, wymagania i lista braków.

    Zawsze ``WHERE id AND shelter_id``; karta innej placówki daje ``None``.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int, animal_id: int) -> dict | None:
        row = self.connection.execute(
            text(f"""
                SELECT a.*, {NEEDS_CONFIRMATION_SQL} AS needs_confirmation,
                       u.first_name AS confirmed_by_first_name,
                       u.last_name AS confirmed_by_last_name
                FROM animals a
                LEFT JOIN users u ON u.id = a.last_confirmed_by
                WHERE a.id = :id AND a.shelter_id = :shelter_id
            """),
            {"id": animal_id, "shelter_id": shelter_id},
        ).mappings().first()
        if row is None:
            return None
        animal = dict(row)

        photos = self.connection.execute(
            text("""
                SELECT id, file_path, alt_text, position, is_main
                FROM animal_photos WHERE animal_id = :id
                ORDER BY position, id
            """),
            {"id": animal_id},
        ).mappings().all()
        requirements = self.connection.execute(
            text("SELECT * FROM animal_care_requirements WHERE animal_id = :id"),
            {"id": animal_id},
        ).mappings().first()

        animal["photos"] = [dict(p) for p in photos]
        animal["requirements"] = dict(requirements) if requirements else None
        animal["missing"] = missing_for_publication(animal, len(animal["photos"]))
        return animal