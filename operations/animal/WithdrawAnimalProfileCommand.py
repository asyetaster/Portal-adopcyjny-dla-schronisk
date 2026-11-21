from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import PUBLISHED_STATUSES, ensure_shelter_writable, get_shelter_animal
from operations.common import end_animal_activity
from operations.errors import BusinessRuleError


class WithdrawAnimalProfileCommand:
    """Opublikowana karta → ``Withdrawn`` z powodem + skutki z R7.

    Szkicu nie wycofujemy: nigdy nie był opublikowany, więc nie ma czego
    wycofywać (schemat wymaga ``published_at`` dla każdego statusu poza ``Draft``).
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, *, actor_id: int, shelter_id: int, animal_id: int, reason: str) -> None:
        ensure_shelter_writable(self.connection, shelter_id)
        animal = get_shelter_animal(self.connection, shelter_id, animal_id)

        reason = reason.strip()
        if not reason:
            raise BusinessRuleError("Podaj powód wycofania karty.")
        if len(reason) > 1000:
            raise BusinessRuleError("Powód: maksymalnie 1000 znaków.")
        if animal["status"] not in PUBLISHED_STATUSES:
            raise BusinessRuleError("Wycofać można tylko opublikowaną kartę.")

        self.connection.execute(
            text("""
                UPDATE animals
                SET
                    status = 'Withdrawn',
                    withdrawn_reason = :reason,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE id = :animal_id AND shelter_id = :shelter_id
            """),
            {"animal_id": animal_id, "shelter_id": shelter_id, "reason": reason},
        )
        end_animal_activity(self.connection, animal_id, reason)