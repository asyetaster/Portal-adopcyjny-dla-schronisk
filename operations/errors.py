"""Błędy zgłaszane przez operacje.

Obsługuje je ``routes/errors.py``: ``BusinessRuleError`` → flash + powrót,
``NotFoundError`` → 404.
"""


class NotFoundError(Exception):
    """Szukany rekord nie istnieje."""


class BusinessRuleError(Exception):
    """Naruszenie reguły biznesowej. Komunikat jest gotowy do pokazania użytkownikowi."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
