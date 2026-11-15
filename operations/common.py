"""Wspólny kod operacji. Rozbudowywany w kolejnych milestone'ach.

Na razie tylko ``now_utc()``. Później dojdą m.in. fragmenty SQL z warunkami
widoczności, ``record_event()`` i ``end_animal_activity()``.
"""

from datetime import datetime, timezone

# Taki sam format jak domyślne wartości kolumn w schema.sql.
ISO_UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def now_utc() -> str:
    """Aktualny czas jako ISO-8601 UTC, np. ``2026-11-08T12:30:00Z``."""
    return datetime.now(timezone.utc).strftime(ISO_UTC_FORMAT)
