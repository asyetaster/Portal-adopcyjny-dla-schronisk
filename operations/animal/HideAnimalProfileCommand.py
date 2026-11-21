from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError


class HideAnimalProfileCommand:
    """Admin: ukrycie karty w katalogu. Tylko flaga (R6, D13), status bez zmian.

    Placówka dalej widzi kartę w panelu i może ją edytować.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, animal_id: int, reason: str) -> None:
        reason = reason.strip()
        if not reason:
            raise BusinessRuleError("Podaj powód ukrycia karty.")
        if len(reason) > 1000:
            raise BusinessRuleError("Powód: maksymalnie 1000 znaków.")

        is_hidden = self.connection.execute(
            text("SELECT is_hidden FROM animals WHERE id = :id"), {"id": animal_id}
        ).scalar_one_or_none()
        if is_hidden is None:
            raise NotFoundError()
        if is_hidden:
            raise BusinessRuleError("Karta jest już ukryta.")

        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    is_hidden = 1,
                    hidden_reason = :reason,
                    hidden_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
                    hidden_by = :actor_id,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id
            """),
            {"animal_id": animal_id, "reason": reason, "actor_id": actor_id},
        )