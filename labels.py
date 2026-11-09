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
        "Pending": "Oczekuje na akceptację",
        "Approved": "Zatwierdzone",
        "Rejected": "Odrzucone",
        "Blocked": "Zablokowane",
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
