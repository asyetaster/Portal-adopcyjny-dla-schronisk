"""Moduł kart zwierząt (M3): stałe, walidacja pól i wspólne zapytania pomocnicze."""

from sqlalchemy import text

from operations.errors import BusinessRuleError, NotFoundError
from operations.shelter import get_shelter_status

SPECIES = ("Dog", "Cat")
SEXES = ("Male", "Female", "Unknown")
SIZES = ("Small", "Medium", "Large")
TRI_STATES = ("Yes", "No", "Unknown")
ACTIVITY_LEVELS = ("Low", "Medium", "High")
EXPERIENCE_LEVELS = ("None", "Basic", "Experienced")

MAX_NAME_LENGTH = 100
MAX_TEXT_LENGTH = 5000
MAX_AGE_MONTHS = 600  # 50 lat; odcina literówki typu 9999

# Statusy, w których karta jest opublikowana (widoczna, o ile nie ukryta).
PUBLISHED_STATUSES = ("Available", "AdoptionInProgress")


def ensure_shelter_writable(connection, shelter_id: int) -> str:
    """Zablokowana placówka ma panel tylko do odczytu (R5). Zwraca status placówki."""
    status = get_shelter_status(connection, shelter_id)
    if status == "Blocked":
        raise BusinessRuleError("Placówka jest zablokowana — panel działa tylko do odczytu.")
    return status


def get_shelter_animal(connection, shelter_id: int, animal_id: int) -> dict:
    """Karta z danej placówki albo ``NotFoundError``.

    Każda operacja panelu zaczyna od tego: ``WHERE id AND shelter_id`` sprawia,
    że podmiana ID w adresie nie da dostępu do karty innej placówki (BR-049, AC-005).
    """
    row = connection.execute(
        text("SELECT * FROM animals WHERE id = :id AND shelter_id = :shelter_id"),
        {"id": animal_id, "shelter_id": shelter_id},
    ).mappings().first()
    if row is None:
        raise NotFoundError()
    return dict(row)


def clean_text(value: str, label: str, *, max_length: int = MAX_TEXT_LENGTH) -> str:
    value = value.strip()
    if len(value) > max_length:
        raise BusinessRuleError(f"{label}: maksymalnie {max_length} znaków.")
    return value


def optional_text(value: str, label: str) -> str | None:
    """Pusty tekst zapisujemy jako NULL (zasady wspólne, pkt 2)."""
    return clean_text(value, label) or None


def choice(value: str, allowed: tuple[str, ...], label: str) -> str:
    value = value.strip()
    if value not in allowed:
        raise BusinessRuleError(f"{label}: niepoprawna wartość.")
    return value


def optional_choice(value: str, allowed: tuple[str, ...], label: str) -> str | None:
    value = value.strip()
    return choice(value, allowed, label) if value else None


def age_range(age_min_months: int, age_max_months: int) -> tuple[int | None, int | None]:
    """Przedział wieku w miesiącach; ``-1`` = brak (zasady wspólne, pkt 2).

    Podana tylko jedna granica oznacza wiek dokładny (obie granice równe).
    Obie puste: wiek nieznany (NULL, NULL).
    """
    for value in (age_min_months, age_max_months):
        if value < -1 or value > MAX_AGE_MONTHS:
            raise BusinessRuleError(f"Wiek: podaj liczbę miesięcy od 0 do {MAX_AGE_MONTHS}.")
    low = age_min_months if age_min_months >= 0 else None
    high = age_max_months if age_max_months >= 0 else None
    if low is None and high is None:
        return None, None
    if low is None:
        low = high
    if high is None:
        high = low
    if low > high:
        raise BusinessRuleError("Wiek: dolna granica nie może być większa od górnej.")
    return low, high


def normalize_tags(value: str) -> str | None:
    """Temperament jako tagi rozdzielone przecinkami, bez pustych i duplikatów."""
    tags: list[str] = []
    for tag in value.split(","):
        tag = " ".join(tag.split())
        if tag and tag.lower() not in (t.lower() for t in tags):
            tags.append(tag)
    joined = ",".join(tags)
    if len(joined) > 200:
        raise BusinessRuleError("Temperament: maksymalnie 200 znaków.")
    return joined or None


def missing_for_publication(animal: dict, photo_count: int) -> list[str]:
    """Braki blokujące publikację (BR-008). Pusta lista = można publikować.

    ``Unknown`` przy płci jest dozwolone („nieustalone” zamiast przypuszczeń),
    ale wiek, wielkość, opis i potrzeby muszą być uzupełnione.
    """
    missing = []
    if not animal["description"].strip():
        missing.append("opis charakteru")
    if not animal["daily_needs"].strip():
        missing.append("codzienne potrzeby")
    if animal["age_min_months"] is None:
        missing.append("wiek lub przedział wieku")
    if animal["size"] is None:
        missing.append("wielkość")
    if photo_count < 1:
        missing.append("co najmniej jedno zdjęcie")
    return missing


def count_photos(connection, animal_id: int) -> int:
    return connection.execute(
        text("SELECT COUNT(*) FROM animal_photos WHERE animal_id = :id"),
        {"id": animal_id},
    ).scalar_one()