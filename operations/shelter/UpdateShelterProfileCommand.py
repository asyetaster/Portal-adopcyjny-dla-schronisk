from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError
from operations.shelter import get_shelter_status, shelter_params


class UpdateShelterProfileCommand:
    """Edycja profilu placówki z panelu (pełna zamiana pól). Zablokowana: tylko odczyt (R5)."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
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
    ) -> None:
        if get_shelter_status(self.connection, shelter_id) == "Blocked":
            raise BusinessRuleError("Placówka jest zablokowana — panel działa tylko do odczytu.")

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

        self.connection.execute(
            text("""
                UPDATE shelters
                SET
                    name = :name,
                    description = :description,
                    street_address = :street_address,
                    postal_code = :postal_code,
                    city = :city,
                    voivodeship = :voivodeship,
                    contact_email = :contact_email,
                    contact_phone = :contact_phone,
                    website = :website,
                    adoption_rules = :adoption_rules,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {**params, "shelter_id": shelter_id},
        )
