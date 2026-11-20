from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal import (
    ACTIVITY_LEVELS,
    EXPERIENCE_LEVELS,
    TRI_STATES,
    choice,
    ensure_shelter_writable,
    get_shelter_animal,
    optional_choice,
    optional_text,
)


class UpdateAnimalCareRequirementsCommand:
    """Upsert wymagań opiekuńczych: źródło dla dopasowania w M4 (D4).

    ``Unknown`` to co innego niż ``No`` (BR-010) i dopasowanie nigdy
    nie zamieni go w zgodność.
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(
        self,
        *,
        actor_id: int,
        shelter_id: int,
        animal_id: int,
        good_with_children: str,
        good_with_dogs: str,
        good_with_cats: str,
        special_care_required: str,
        activity_level: str = "",
        min_experience: str = "",
        special_care_notes: str = "",
        notes_to_discuss: str = "",
    ) -> None:
        ensure_shelter_writable(self.connection, shelter_id)
        get_shelter_animal(self.connection, shelter_id, animal_id)

        self.connection.execute(
            text("""
                INSERT INTO animal_care_requirements (
                    animal_id, good_with_children, good_with_dogs, good_with_cats,
                    activity_level, min_experience, special_care_required,
                    special_care_notes, notes_to_discuss, updated_by
                )
                VALUES (
                    :animal_id, :children, :dogs, :cats,
                    :activity, :experience, :special_care,
                    :care_notes, :to_discuss, :actor_id
                )
                ON CONFLICT (animal_id) DO UPDATE SET
                    good_with_children = excluded.good_with_children,
                    good_with_dogs = excluded.good_with_dogs,
                    good_with_cats = excluded.good_with_cats,
                    activity_level = excluded.activity_level,
                    min_experience = excluded.min_experience,
                    special_care_required = excluded.special_care_required,
                    special_care_notes = excluded.special_care_notes,
                    notes_to_discuss = excluded.notes_to_discuss,
                    updated_by = excluded.updated_by,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
            """),
            {
                "animal_id": animal_id,
                "actor_id": actor_id,
                "children": choice(good_with_children, TRI_STATES, "Dzieci"),
                "dogs": choice(good_with_dogs, TRI_STATES, "Psy"),
                "cats": choice(good_with_cats, TRI_STATES, "Koty"),
                "special_care": choice(special_care_required, TRI_STATES, "Szczególna opieka"),
                "activity": optional_choice(activity_level, ACTIVITY_LEVELS, "Aktywność"),
                "experience": optional_choice(min_experience, EXPERIENCE_LEVELS, "Doświadczenie"),
                "care_notes": optional_text(special_care_notes, "Opis szczególnej opieki"),
                "to_discuss": optional_text(notes_to_discuss, "Kwestie do omówienia"),
            },
        )