from sqlalchemy import text
from sqlalchemy.engine import Connection


class GetShelterProfileQuery:
    """Publiczny profil placówki; None, gdy placówka nie jest zatwierdzona."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int) -> dict | None:
        row = self.connection.execute(
            text("""
                SELECT
                    id, name, description, street_address, postal_code, city,
                    voivodeship, contact_email, contact_phone, website, adoption_rules
                FROM shelters
                WHERE id = :id AND status = 'Approved'
            """),
            {"id": shelter_id},
        ).mappings().first()
        return dict(row) if row is not None else None
