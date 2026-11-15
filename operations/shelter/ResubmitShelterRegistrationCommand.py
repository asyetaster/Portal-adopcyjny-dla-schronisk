from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError
from operations.shelter import get_employment, shelter_params


class ResubmitShelterRegistrationCommand:
    """Ponowne zgłoszenie odrzuconej placówki (Rejected → Pending), tylko kierownik."""

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
        employment = get_employment(self.connection, shelter_id, actor_id)
        if employment is None:
            raise NotFoundError()
        if not employment["is_manager"]:
            raise BusinessRuleError("Zgłoszenie może ponowić tylko kierownik placówki.")
        if employment["status"] != "Rejected":
            raise BusinessRuleError("Ponownie zgłosić można tylko odrzuconą placówkę.")

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
                    status = 'Pending',
                    rejection_reason = NULL,
                    decided_by = NULL,
                    decided_at = NULL,
                    submitted_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :shelter_id
            """),
            {**params, "shelter_id": shelter_id},
        )
