"""Polskie etykiety wartości enumów z schema.sql - jedno miejsce.

W szablonach: ``{{ application.status|label("adoption") }}``.
Brak etykiety => zwracana jest sama wartość (nic się nie wysypuje),
``None`` => myślnik.
"""

LABELS: dict[str, dict[str, str]] = {
    "user": {
        "Active": "Aktywny",
        "Blocked": "Zablokowany",
        "Anonymized": "Zanonimizowany",
    },
    "shelter": {
        "Pending": "Oczekuje na zatwierdzenie",
        "Approved": "Zatwierdzona",
        "Rejected": "Odrzucona",
        "Blocked": "Zablokowana",
    },
    "animal": {
        "Draft": "Szkic",
        "Available": "Do adopcji",
        "AdoptionInProgress": "W trakcie adopcji",
        "Adopted": "Adoptowane",
        "Withdrawn": "Wycofane",
    },
    "species": {"Dog": "Pies", "Cat": "Kot"},
    "sex": {"Male": "Samiec", "Female": "Samica", "Unknown": "Nieznana"},
    "size": {"Small": "Mały", "Medium": "Średni", "Large": "Duży"},
    "tri_state": {"Yes": "Tak", "No": "Nie", "Unknown": "Nieznane"},
    "activity": {"Low": "Niska", "Medium": "Średnia", "High": "Wysoka"},
    "experience": {
        "None": "Brak",
        "Basic": "Podstawowe",
        "Experienced": "Doświadczony",
    },
    "adoption_type": {"Portal": "Przez portal", "External": "Poza portalem"},
    "adoption": {
        "Submitted": "Złożone",
        "InContact": "W kontakcie",
        "Withdrawn": "Wycofane",
        "ClosedWithoutAdoption": "Zamknięte bez adopcji",
        "Adopted": "Zakończone adopcją",
    },
    "volunteering": {
        "Submitted": "Złożone",
        "InContact": "W kontakcie",
        "Accepted": "Przyjęte",
        "Rejected": "Odrzucone",
        "Withdrawn": "Wycofane",
        "Ended": "Zakończone",
    },
    "walk_slot": {
        "Open": "Wolny",
        "Reserved": "Zarezerwowany",
        "Vacated": "Zwolniony",
        "Cancelled": "Anulowany",
        "Completed": "Odbyty",
        "NoShow": "Nieobecność",
    },
    "walk_application": {
        "Pending": "Oczekuje",
        "Accepted": "Zaakceptowane",
        "Rejected": "Odrzucone",
        "Withdrawn": "Wycofane",
        "SlotTaken": "Termin zajęty",
        "CancelledByShelter": "Anulowane przez schronisko",
        "Completed": "Odbyty",
        "NoShow": "Nieobecność",
    },
    "donation": {
        "Pending": "Oczekuje",
        "Succeeded": "Opłacona",
        "Failed": "Nieudana",
        "Cancelled": "Anulowana",
        "PartiallyRefunded": "Częściowo zwrócona",
        "Refunded": "Zwrócona",
    },
    "event_type": {"StatusChange": "Zmiana statusu", "Message": "Wiadomość"},
}


def label(value: str | None, group: str) -> str:
    if value is None:
        return "—"
    return LABELS.get(group, {}).get(value, value)


def _years(n: int) -> str:
    if n == 1:
        return "1 rok"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return f"{n} lata"
    return f"{n} lat"


def _age_part(months: int) -> str:
    if months < 12:
        return f"{months} mies."
    years, rest = divmod(months, 12)
    return _years(years) + (f" {rest} mies." if rest else "")


def format_age(age_min_months: int | None, age_max_months: int | None) -> str:
    """Wiek lub przedział wieku po polsku: ``8 mies.``, ``2 lata``, ``2 lata – 3 lata``."""
    if age_min_months is None or age_max_months is None:
        return "wiek nieustalony"
    if age_min_months == age_max_months:
        return _age_part(age_min_months)
    return f"{_age_part(age_min_months)} – {_age_part(age_max_months)}"