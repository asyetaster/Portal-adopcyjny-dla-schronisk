from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.animal.UpdateAnimalProfileCommand import UpdateAnimalProfileCommand
from routes.animal import read_animal_form
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>")
    @shelter_required(write=True)
    @page("panel/animals/edit.html", write=True)
    def panel_animal_update(shelter_id: int, animal_id: int, update: UpdateAnimalProfileCommand):
        update.execute(
            actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id,
            **read_animal_form(),
        )
        flash("Zapisano dane karty.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )