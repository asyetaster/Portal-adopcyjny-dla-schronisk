"""Trasy kart zwierząt (M3): katalog publiczny, panel placówki, moderacja.

Tu leżą helpery wspólne dla wszystkich plików w tym katalogu: czytanie
formularzy i obsługa plików zdjęć.
"""

import uuid
from pathlib import Path

from flask import abort, current_app, request

from operations.errors import BusinessRuleError

MAX_PHOTO_BYTES = 5 * 1024 * 1024
UPLOAD_SUBDIR = "uploads/animals"


def read_int(name: str, default: int = -1) -> int:
    """Liczba całkowita z formularza; puste pole = ``default``, śmieci = 400."""
    raw = request.form.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        abort(400, description=f"Pole {name}: podaj liczbę całkowitą")


def read_animal_form() -> dict:
    """Dane podstawowe karty. Wartości i długości sprawdza operacja."""
    data = {
        field: request.form.get(field, "").strip()
        for field in (
            "name", "species", "sex", "description", "daily_needs",
            "breed", "size", "temperament",
        )
    }
    data["age_min_months"] = read_int("age_min_months")
    data["age_max_months"] = read_int("age_max_months")
    return data


def read_requirements_form() -> dict:
    return {
        field: request.form.get(field, "").strip()
        for field in (
            "good_with_children", "good_with_dogs", "good_with_cats",
            "special_care_required", "activity_level", "min_experience",
            "special_care_notes", "notes_to_discuss",
        )
    }


# --- Pliki zdjęć --------------------------------------------------------------

def _detect_image_type(head: bytes) -> str | None:
    """Typ po sygnaturze pliku, nie po rozszerzeniu ani nagłówku od klienta."""
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


def save_photo(file) -> str:
    """Zapisuje wgrane zdjęcie i zwraca ścieżkę względną wobec ``static/``.

    Tylko jpg / png / webp, maks. 5 MB. Błędy to ``BusinessRuleError``
    (flash + powrót na formularz).
    """
    if file is None or not file.filename:
        raise BusinessRuleError("Wybierz plik ze zdjęciem.")
    data = file.read(MAX_PHOTO_BYTES + 1)
    if len(data) > MAX_PHOTO_BYTES:
        raise BusinessRuleError("Zdjęcie jest za duże (maksymalnie 5 MB).")
    extension = _detect_image_type(data[:12])
    if extension is None:
        raise BusinessRuleError("Dozwolone formaty zdjęć: JPG, PNG, WebP.")

    relative = f"{UPLOAD_SUBDIR}/{uuid.uuid4().hex}.{extension}"
    target = Path(current_app.static_folder) / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return relative


def delete_photo_file(relative_path: str) -> None:
    """Kasuje plik wgrany przez ``save_photo``.

    Pliki spoza ``static/uploads/animals/`` (np. zdjęcia demo w ``static/img/``)
    zostają nietknięte.
    """
    upload_dir = (Path(current_app.static_folder) / UPLOAD_SUBDIR).resolve()
    target = (Path(current_app.static_folder) / relative_path).resolve()
    if target.parent == upload_dir:
        target.unlink(missing_ok=True)