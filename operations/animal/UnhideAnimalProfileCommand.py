from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.errors import BusinessRuleError, NotFoundError


class UnhideAnimalProfileCommand:
    """Admin: przywrócenie ukrytej karty do katalogu."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, animal_id: int) -> None:
        is_hidden = self.connection.execute(
            text("SELECT is_hidden FROM animals WHERE id = :id"), {"id": animal_id}
        ).scalar_one_or_none()
        if is_hidden is None:
            raise NotFoundError()
        if not is_hidden:
            raise BusinessRuleError("Karta nie jest ukryta.")

        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    is_hidden = 0,
                    hidden_reason = NULL,
                    hidden_at = NULL,
                    hidden_by = NULL,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id
            """),
            {"animal_id": animal_id},
        )