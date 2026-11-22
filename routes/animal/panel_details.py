from flask import Flask, abort

from auth import shelter_required
from operations.animal.GetAnimalProfileForManagementQuery import (
    GetAnimalProfileForManagementQuery,
)
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>")
    @shelter_required()
    @page("panel/animals/details.html")
    def panel_animal_details(
        shelter_id: int, animal_id: int, get_animal: GetAnimalProfileForManagementQuery
    ):
        animal = get_animal.execute(shelter_id, animal_id)
        if animal is None:
            abort(404)
        return {"animal": animal}