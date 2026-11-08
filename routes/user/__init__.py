"""Trasy dotyczące użytkowników."""

import re
import sqlite3

from flask import abort, request
from sqlalchemy.exc import IntegrityError

from operations.errors import BusinessRuleError
from operations.user import MAX_EMAIL_LENGTH, MAX_NAME_LENGTH


EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def read_required_text(
    field: str,
    label: str,
    max_length: int,
) -> str:
    value = request.form.get(field, "").strip()

    if not value:
        abort(400, description=f"{label}: pole nie może być puste")

    if len(value) > max_length:
        abort(
            400,
            description=f"{label}: maksymalnie {max_length} znaków",
        )

    return value


def read_user_form(*, creating: bool) -> dict:
    first_name = read_required_text(
        "first_name",
        "Imię",
        MAX_NAME_LENGTH,
    )
    last_name = read_required_text(
        "last_name",
        "Nazwisko",
        MAX_NAME_LENGTH,
    )
    email = read_required_text(
        "email",
        "E-mail",
        MAX_EMAIL_LENGTH,
    )

    if not EMAIL_PATTERN.fullmatch(email):
        abort(400, description="Podaj poprawny adres e-mail")

    phone = request.form.get("phone", "").strip()

    # Nie usuwamy spacji z hasła.
    password = request.form.get("password", "")

    if creating and not password:
        abort(400, description="Hasło nie może być puste")

    return {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "is_admin": request.form.get("is_admin") == "1",
        "password": password,
    }


def read_profile_form() -> dict:
    """Pola z formularza „Mój profil” (bez e-maila i hasła)."""
    return {
        "first_name": read_required_text("first_name", "Imię", MAX_NAME_LENGTH),
        "last_name": read_required_text("last_name", "Nazwisko", MAX_NAME_LENGTH),
        "phone": request.form.get("phone", "").strip(),
    }


def read_register_form() -> dict:
    """Pola z formularza rejestracji. Telefon opcjonalny (BR-050)."""
    data = read_profile_form()

    email = read_required_text("email", "E-mail", MAX_EMAIL_LENGTH)
    if not EMAIL_PATTERN.fullmatch(email):
        abort(400, description="Podaj poprawny adres e-mail")

    # Nie usuwamy spacji z hasła.
    # Długość hasła sprawdza RegisterUserCommand.
    password = request.form.get("password", "")
    if password != request.form.get("password_confirm", ""):
        raise BusinessRuleError("Hasła nie są takie same.")

    return {**data, "email": email, "password": password}


def handle_user_integrity_error(error: IntegrityError) -> None:
    original = error.orig

    if (
        isinstance(original, sqlite3.IntegrityError)
        and getattr(original, "sqlite_errorcode", None)
        == sqlite3.SQLITE_CONSTRAINT_UNIQUE
        and "users.email" in str(original)
    ):
        abort(
            409,
            description="Użytkownik z takim adresem e-mail już istnieje",
        )

    raise error