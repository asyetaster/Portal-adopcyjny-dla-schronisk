"""Wspólny kod operacji. Rozbudowywany w kolejnych milestone'ach.

Teraz: ``now_utc()``, fragmenty SQL z warunkami widoczności kart zwierząt
i ``end_animal_activity()``. Później dojdzie m.in. ``record_event()`` (M5).
"""

from datetime import datetime, timezone

from sqlalchemy import text

# Taki sam format jak domyślne wartości kolumn w schema.sql.
ISO_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# BR-045: po tylu dniach bez potwierdzenia karta dostaje ostrzeżenie.
CONFIRMATION_THRESHOLD_DAYS = 30

# Karta widoczna publicznie (BR-012, R6, D13). Używać w zapytaniach, które
# łączą ``animals a`` z ``shelters s``. Szkic, wycofana, adoptowana, ukryta
# przez administratora albo z niezatwierdzonej / zablokowanej placówki: nie.
VISIBLE_ANIMAL_SQL = """
    a.status IN ('Available', 'AdoptionInProgress')
    AND a.is_hidden = 0
    AND s.status = 'Approved'
"""

# Kolumna 0/1: karta bez potwierdzenia aktualności od ponad 30 dni (BR-045).
# Dla szkicu (last_confirmed_at IS NULL) zawsze 0.
NEEDS_CONFIRMATION_SQL = f"""
    CASE
        WHEN a.last_confirmed_at IS NOT NULL
         AND a.last_confirmed_at < strftime('%Y-%m-%dT%H:%M:%SZ', 'now',
                                            '-{CONFIRMATION_THRESHOLD_DAYS} days')
        THEN 1 ELSE 0
    END
"""

# Zdjęcie na listy i karty: główne, a gdyby go zabrakło, pierwsze z kolei.
MAIN_PHOTO_PATH_SQL = """
    (SELECT p.file_path FROM animal_photos p
      WHERE p.animal_id = a.id
      ORDER BY p.is_main DESC, p.position, p.id LIMIT 1)
"""
MAIN_PHOTO_ALT_SQL = MAIN_PHOTO_PATH_SQL.replace("p.file_path", "p.alt_text")


def now_utc() -> str:
    """Aktualny czas jako ISO-8601 UTC, np. ``2026-11-08T12:30:00Z``."""
    return datetime.now(timezone.utc).strftime(ISO_UTC_FORMAT)


def end_animal_activity(connection, animal_id: int, reason: str) -> None:
    """R7: skutki zakończenia aktywności karty (wycofanie, adopcja).

    M3: wyłącza zbiórkę wpłat na zwierzę. Kolejne milestone'y dopisują tu:
    M5 zamykanie otwartych zgłoszeń adopcyjnych (+ zdarzenie i mail),
    M7 anulowanie przyszłych terminów spacerów.
    ``reason`` jest już teraz w sygnaturze, bo użyje go M5 w zdarzeniu.
    """
    connection.execute(
        text("UPDATE animals SET donations_enabled = 0 WHERE id = :id"),
        {"id": animal_id},
    )