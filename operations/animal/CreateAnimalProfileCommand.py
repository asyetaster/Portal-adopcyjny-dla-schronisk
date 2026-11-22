from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    MAX_NAME_LENGTH,
    SPECIES,
    choice,
    ensure_shelter_writable,
)
from operations.errors import BusinessRuleError


class CreateAnimalProfileCommand:
    """Nowa karta jako szkic. Działa też dla placówki Pending (R3)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, name: str, species: str) -> int:
        ensure_shelter_writable(self.connection, shelter_id)

        name = name.strip()
        if not name:
            raise BusinessRuleError("Imię: pole nie może być puste.")
        if len(name) > MAX_NAME_LENGTH:
            raise BusinessRuleError(f"Imię: maksymalnie {MAX_NAME_LENGTH} znaków.")
        species = choice(species, SPECIES, "Gatunek")

        result = self.connection.execute(
            text("""
                INSERT INTO animals (shelter_id, name, species, status)
                VALUES (:shelter_id, :name, :species, 'Draft')
            """),
            {"shelter_id": shelter_id, "name": name, "species": species},
        )
        animal_id = result.lastrowid
        if animal_id is None:
            raise RuntimeError("Nie udało się odczytać ID karty")
        return animal_id