from flask import Flask, abort

from auth import shelter_required
from labels import LABELS
from operations.animal.GetAnimalProfileForManagementQuery import (
    GetAnimalProfileForManagementQuery,
)
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/requirements")
    @shelter_required()
    @page("panel/animals/requirements.html")
    def panel_animal_requirements_edit(
        shelter_id: int, animal_id: int, get_animal: GetAnimalProfileForManagementQuery
    ):
        animal = get_animal.execute(shelter_id, animal_id)
        if animal is None:
            abort(404)
        return {
            "animal": animal,
            "tri_state_labels": LABELS["tri_state"],
            "activity_labels": LABELS["activity"],
            "experience_labels": LABELS["experience"],
        }