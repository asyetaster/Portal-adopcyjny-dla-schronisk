from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import ensure_shelter_writable, get_shelter_animal
from operations.errors import NotFoundError


class SetMainAnimalPhotoCommand:
    """Zmienia zdjęcie główne: zerowanie i ustawienie w jednej transakcji."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, shelter_id: int, animal_id: int, photo_id: int) -> None:
        ensure_shelter_writable(self.connection, shelter_id)
        get_shelter_animal(self.connection, shelter_id, animal_id)

        exists = self.connection.execute(
            text("SELECT 1 FROM animal_photos WHERE id = :id AND animal_id = :animal_id"),
            {"id": photo_id, "animal_id": animal_id},
        ).first()
        if exists is None:
            raise NotFoundError()

        self.connection.execute(
            text("UPDATE animal_photos SET is_main = 0 WHERE animal_id = :animal_id"),
            {"animal_id": animal_id},
        )
        self.connection.execute(
            text("UPDATE animal_photos SET is_main = 1 WHERE id = :id"), {"id": photo_id}
        )