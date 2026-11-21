from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    PUBLISHED_STATUSES,
    count_photos,
    ensure_shelter_writable,
    get_shelter_animal,
)
from operations.errors import BusinessRuleError, NotFoundError


class RemoveAnimalPhotoCommand:
    """Usuwa wiersz zdjęcia i zwraca ``file_path``, żeby route skasował plik.

    Nie pozwala usunąć ostatniego zdjęcia opublikowanej karty (BR-008).
    Gdy usunięto zdjęcie główne, główne zostaje następne z kolei.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, shelter_id: int, animal_id: int, photo_id: int) -> str:
        ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)

        photo = self.connection.execute(
            text("SELECT file_path, is_main FROM animal_photos WHERE id = :id AND animal_id = :animal_id"),
            {"id": photo_id, "animal_id": animal_id},
        ).mappings().first()
        if photo is None:
            raise NotFoundError()

        if animal["status"] in PUBLISHED_STATUSES and count_photos(self.connection, animal_id) <= 1:
            raise BusinessRuleError(
                "Opublikowana karta musi mieć co najmniej jedno zdjęcie. "
                "Najpierw dodaj nowe albo wycofaj kartę."
            )

        self.connection.execute(
            text("DELETE FROM animal_photos WHERE id = :id"), {"id": photo_id}
        )
        if photo["is_main"]:
            # Usunięcie najpierw, wybór potem: indeks ux_animal_photos_main
            # nie dopuszcza dwóch zdjęć głównych naraz.
            self.connection.execute(
                text("""
                    UPDATE animal_photos SET is_main = 1
                    WHERE id = (
                        SELECT id FROM animal_photos
                        WHERE animal_id = :animal_id ORDER BY position, id LIMIT 1
                    )
                """),
                {"animal_id": animal_id},
            )
        return photo["file_path"]