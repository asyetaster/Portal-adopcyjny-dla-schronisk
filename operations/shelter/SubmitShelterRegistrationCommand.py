from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.shelter import shelter_params


class SubmitShelterRegistrationCommand:
    """Zgłoszenie nowej placówki: status Pending + zgłaszający jako kierownik (D1)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        name: str,
        street_address: str,
        postal_code: str,
        city: str,
        voivodeship: str,
        contact_email: str,
        description: str = "",
        adoption_rules: str = "",
        contact_phone: str = "",
        website: str = "",
    ) -> int:
        params = shelter_params(
            name=name,
            street_address=street_address,
            postal_code=postal_code,
            city=city,
            voivodeship=voivodeship,
            contact_email=contact_email,
            description=description,
            adoption_rules=adoption_rules,
            contact_phone=contact_phone,
            website=website,
        )

        result = self.connection.execute(
            text("""
                INSERT INTO shelters (
                    name, description, street_address, postal_code, city,
                    voivodeship, contact_email, contact_phone, website,
                    adoption_rules, status, submitted_by
                )
                VALUES (
                    :name, :description, :street_address, :postal_code, :city,
                    :voivodeship, :contact_email, :contact_phone, :website,
                    :adoption_rules, 'Pending', :actor_id
                )
            """),
            {**params, "actor_id": actor_id},
        )
        shelter_id = result.lastrowid
        if shelter_id is None:
            raise RuntimeError("Nie udało się odczytać ID placówki")

        self.connection.execute(
            text("""
                INSERT INTO shelter_employees (shelter_id, user_id, is_manager, assigned_by)
                VALUES (:shelter_id, :user_id, 1, :user_id)
            """),
            {"shelter_id": shelter_id, "user_id": actor_id},
        )
        return shelter_id
