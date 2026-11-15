"""Trasy placówek (M2): katalog publiczny, „Moje placówki”, panel placówki, admin."""

from flask import request

from operations.errors import BusinessRuleError
from routes.user import EMAIL_PATTERN

SHELTER_FIELDS = (
    "name",
    "street_address",
    "postal_code",
    "city",
    "voivodeship",
    "contact_email",
    "description",
    "adoption_rules",
    "contact_phone",
    "website",
)


def read_shelter_form() -> dict:
    """Pola profilu placówki z formularza.

    Wymagalność, długości i województwo sprawdza operacja (``shelter_params``);
    tu tylko format adresu e-mail.
    """
    data = {field: request.form.get(field, "").strip() for field in SHELTER_FIELDS}
    if data["contact_email"] and not EMAIL_PATTERN.fullmatch(data["contact_email"]):
        raise BusinessRuleError("Podaj poprawny e-mail kontaktowy.")
    return data
