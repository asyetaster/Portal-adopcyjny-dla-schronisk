from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    MAX_NAME_LENGTH,
    SEXES,
    SIZES,
    SPECIES,
    age_range,
    choice,
    clean_text,
    ensure_shelter_writable,
    get_shelter_animal,
    normalize_tags,
    optional_choice,
    optional_text,
)
from operations.errors import BusinessRuleError


class UpdateAnimalProfileCommand:
    """Pełna zamiana danych podstawowych karty. Nie zmienia statusu ani aktualności.

    Zmiana opisu nie zastępuje potwierdzenia aktualności (BR-044), więc
    ``last_confirmed_*`` zostaje nietknięte.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
        animal_id: int,
        name: str,
        species: str,
        sex: str,
        description: str,
        daily_needs: str,
        breed: str = "",
        size: str = "",
        age_min_months: int = -1,
        age_max_months: int = -1,
        temperament: str = "",
    ) -> None:
        ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)
        if animal["status"] == "Adopted":
            raise BusinessRuleError("Karta zakończona adopcją nie podlega edycji.")

        name = name.strip()
        if not name:
            raise BusinessRuleError("Imię: pole nie może być puste.")
        if len(name) > MAX_NAME_LENGTH:
            raise BusinessRuleError(f"Imię: maksymalnie {MAX_NAME_LENGTH} znaków.")
        species = choice(species, SPECIES, "Gatunek")
        if species != animal["species"] and animal["status"] != "Draft":
            raise BusinessRuleError("Gatunek można zmienić tylko w szkicu karty.")
        low, high = age_range(age_min_months, age_max_months)

        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    name = :name,
                    species = :species,
                    sex = :sex,
                    breed = :breed,
                    size = :size,
                    age_min_months = :age_min,
                    age_max_months = :age_max,
                    description = :description,
                    daily_needs = :daily_needs,
                    temperament = :temperament,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id AND shelter_id = :shelter_id
            """),
            {
                "animal_id": animal_id,
                "shelter_id": shelter_id,
                "name": name,
                "species": species,
                "sex": choice(sex, SEXES, "Płeć"),
                "breed": optional_text(breed, "Rasa"),
                "size": optional_choice(size, SIZES, "Wielkość"),
                "age_min": low,
                "age_max": high,
                "description": clean_text(description, "Opis"),
                "daily_needs": clean_text(daily_needs, "Codzienne potrzeby"),
                "temperament": normalize_tags(temperament),
            },
        )