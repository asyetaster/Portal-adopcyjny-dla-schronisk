from flask import Flask, abort

from auth import shelter_required
from labels import LABELS
from operations.animal.GetAnimalProfileForManagementQuery import (
    GetAnimalProfileForManagementQuery,
)
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/edit")
    @shelter_required()
    @page("panel/animals/edit.html")
    def panel_animal_edit(
        shelter_id: int, animal_id: int, get_animal: GetAnimalProfileForManagementQuery
    ):
        animal = get_animal.execute(shelter_id, animal_id)
        if animal is None:
            abort(404)
        return {
            "animal": animal,
            "species_labels": LABELS["species"],
            "sex_labels": LABELS["sex"],
            "size_labels": LABELS["size"],
        }