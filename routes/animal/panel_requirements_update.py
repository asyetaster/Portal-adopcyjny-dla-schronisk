from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.animal.UpdateAnimalCareRequirementsCommand import (
    UpdateAnimalCareRequirementsCommand,
)
from routes.animal import read_requirements_form
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/requirements")
    @shelter_required(write=True)
    @page("panel/animals/requirements.html", write=True)
    def panel_animal_requirements_update(
        shelter_id: int, animal_id: int, update: UpdateAnimalCareRequirementsCommand
    ):
        update.execute(
            actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id,
            **read_requirements_form(),
        )
        flash("Zapisano wymagania opiekuńcze.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )