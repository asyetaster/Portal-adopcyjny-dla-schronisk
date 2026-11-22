from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    PUBLISHED_STATUSES,
    age_range,
    ensure_shelter_writable,
    get_shelter_animal,
)
from operations.errors import BusinessRuleError


class ConfirmAnimalProfileAccuracyCommand:
    """Pracownik potwierdza aktualność karty i statusu (BR-044, D8).

    Zapisuje czas i osobę. Opcjonalnie koryguje wiek: wiek szacowany starzeje
    się razem ze zwierzęciem, więc przy potwierdzeniu najłatwiej go poprawić.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
        animal_id: int,
        age_min_months: int = -1,
        age_max_months: int = -1,
    ) -> None:
        ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)
        if animal["status"] not in PUBLISHED_STATUSES:
            raise BusinessRuleError("Aktualność potwierdza się tylko dla opublikowanej karty.")

        # Oba -1 = bez korekty wieku.
        correct_age = age_min_months >= 0 or age_max_months >= 0
        low, high = age_range(age_min_months, age_max_months)

        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    last_confirmed_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    last_confirmed_by = :actor_id,
                    age_min_months = CASE WHEN :correct_age THEN :age_min ELSE age_min_months END,
                    age_max_months = CASE WHEN :correct_age THEN :age_max ELSE age_max_months END,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id AND shelter_id = :shelter_id
            """),
            {
                "animal_id": animal_id,
                "shelter_id": shelter_id,
                "actor_id": actor_id,
                "correct_age": 1 if correct_age else 0,
                "age_min": low,
                "age_max": high,
            },
        )