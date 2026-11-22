from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    count_photos,
    ensure_shelter_writable,
    get_shelter_animal,
    missing_for_publication,
)
from operations.errors import BusinessRuleError


class PublishAnimalProfileCommand:
    """Szkic albo wycofana karta → ``Available``. Warunki: RB-001 i BR-008."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, animal_id: int) -> None:
        shelter_status = ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)

        if shelter_status != "Approved":
            raise BusinessRuleError(
                "Kartę można opublikować dopiero po zatwierdzeniu placówki przez administratora."
            )
        if animal["status"] not in ("Draft", "Withdrawn"):
            raise BusinessRuleError("Tę kartę nie można opublikować w obecnym statusie.")

        missing = missing_for_publication(animal, count_photos(self.connection, animal_id))
        if missing:
            raise BusinessRuleError("Przed publikacją uzupełnij: " + ", ".join(missing) + ".")

        # Ponowna publikacja po wycofaniu liczy się jak nowa (BR-019) i zeruje powód.
        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    status = 'Available',
                    withdrawn_reason = NULL,
                    published_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    last_confirmed_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    last_confirmed_by = :actor_id,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id AND shelter_id = :shelter_id
            """),
            {"animal_id": animal_id, "shelter_id": shelter_id, "actor_id": actor_id},
        )