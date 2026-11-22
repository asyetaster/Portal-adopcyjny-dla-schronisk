from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    clean_text,
    ensure_shelter_writable,
    get_shelter_animal,
)
from operations.errors import BusinessRuleError

MAX_PHOTOS_PER_ANIMAL = 12


class AddAnimalPhotoCommand:
    """Zapisuje wiersz zdjęcia. Samego pliku nie dotyka: robi to route.

    ``file_path`` jest względny wobec ``static/`` (np. ``uploads/animals/<uuid>.jpg``).
    Pierwsze zdjęcie karty dostaje ``is_main = 1`` (BR-018).
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
        animal_id: int,
        file_path: str,
        alt_text: str = "",
    ) -> int:
        ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)
        if animal["status"] == "Adopted":
            raise BusinessRuleError("Karta zakończona adopcją nie podlega edycji.")
        file_path = file_path.strip()
        if not file_path:
            raise BusinessRuleError("Brak pliku zdjęcia.")

        count, next_position = self.connection.execute(
            text("""
                SELECT COUNT(*), COALESCE(MAX(position), -1) + 1
                FROM animal_photos WHERE animal_id = :id
            """),
            {"id": animal_id},
        ).one()
        if count >= MAX_PHOTOS_PER_ANIMAL:
            raise BusinessRuleError(f"Karta może mieć maksymalnie {MAX_PHOTOS_PER_ANIMAL} zdjęć.")

        result = self.connection.execute(
            text("""
                INSERT INTO animal_photos (animal_id, file_path, alt_text, position, is_main, uploaded_by)
                VALUES (:animal_id, :file_path, :alt_text, :position, :is_main, :actor_id)
            """),
            {
                "animal_id": animal_id,
                "file_path": file_path,
                "alt_text": clean_text(alt_text, "Opis zdjęcia", max_length=200) or None,
                "position": next_position,
                "is_main": 1 if count == 0 else 0,
                "actor_id": actor_id,
            },
        )
        return result.lastrowid