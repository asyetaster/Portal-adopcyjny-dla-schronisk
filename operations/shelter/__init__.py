"""Moduł placówek (M2): stałe i wspólna walidacja pól profilu."""

from operations.errors import BusinessRuleError

VOIVODESHIPS = (
    "dolnośląskie",
    "kujawsko-pomorskie",
    "lubelskie",
    "lubuskie",
    "łódzkie",
    "małopolskie",
    "mazowieckie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "pomorskie",
    "śląskie",
    "świętokrzyskie",
    "warmińsko-mazurskie",
    "wielkopolskie",
    "zachodniopomorskie",
)

MAX_SHELTER_NAME_LENGTH = 200
MAX_FIELD_LENGTH = 200
MAX_TEXT_LENGTH = 5000

REQUIRED_FIELDS = {
    "name": "Nazwa",
    "street_address": "Adres",
    "postal_code": "Kod pocztowy",
    "city": "Miejscowość",
    "voivodeship": "Województwo",
    "contact_email": "E-mail kontaktowy",
}


def shelter_params(
    *,
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
) -> dict:
    """Czyści i sprawdza pola profilu placówki; zwraca parametry do SQL.

    Puste ``contact_phone`` / ``website`` zapisujemy jako NULL.
    """
    values = {
        "name": name.strip(),
        "street_address": street_address.strip(),
        "postal_code": postal_code.strip(),
        "city": city.strip(),
        "voivodeship": voivodeship.strip(),
        "contact_email": contact_email.strip(),
    }
    for field, label in REQUIRED_FIELDS.items():
        if not values[field]:
            raise BusinessRuleError(f"{label}: pole nie może być puste.")
    if len(values["name"]) > MAX_SHELTER_NAME_LENGTH:
        raise BusinessRuleError(
            f"Nazwa: maksymalnie {MAX_SHELTER_NAME_LENGTH} znaków."
        )
    if values["voivodeship"] not in VOIVODESHIPS:
        raise BusinessRuleError("Wybierz województwo z listy.")

    return {
        **values,
        "description": description.strip(),
        "adoption_rules": adoption_rules.strip(),
        "contact_phone": contact_phone.strip() or None,
        "website": website.strip() or None,
    }


def get_employment(connection, shelter_id: int, user_id: int) -> dict | None:
    """Wiersz ``shelter_employees`` + status placówki albo None."""
    from sqlalchemy import text

    row = connection.execute(
        text("""
            SELECT e.is_manager, s.status
            FROM shelter_employees e
            JOIN shelters s ON s.id = e.shelter_id
            WHERE e.shelter_id = :shelter_id AND e.user_id = :user_id
        """),
        {"shelter_id": shelter_id, "user_id": user_id},
    ).mappings().first()
    return dict(row) if row is not None else None


def get_shelter_status(connection, shelter_id: int) -> str:
    """Status placówki; ``NotFoundError``, gdy nie istnieje."""
    from sqlalchemy import text

    from operations.errors import NotFoundError

    status = connection.execute(
        text("SELECT status FROM shelters WHERE id = :id"),
        {"id": shelter_id},
    ).scalar_one_or_none()
    if status is None:
        raise NotFoundError()
    return status
