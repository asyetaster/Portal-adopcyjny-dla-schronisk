"""Trasy dotyczące użytkowników."""

from flask import abort, request

from operations.user import MAX_NAME_LENGTH


def read_user_name(field: str) -> str:
    """Odczytuje nazwę użytkownika z formularza; przy błędzie abort(400)."""
    name = request.form.get(field, "").strip()
    if not name:
        abort(400, description="Nazwa nie może być pusta")
    if len(name) > MAX_NAME_LENGTH:
        abort(400, description=f"Nazwa może mieć najwyżej {MAX_NAME_LENGTH} znaków")
    return name