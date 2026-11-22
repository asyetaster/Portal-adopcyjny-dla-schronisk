from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.animal.ConfirmAnimalProfileAccuracyCommand import (
    ConfirmAnimalProfileAccuracyCommand,
)
from routes.animal import read_int
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/confirm")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_confirm(
        shelter_id: int, animal_id: int, confirm: ConfirmAnimalProfileAccuracyCommand
    ):
        confirm.execute(
            actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id,
            age_min_months=read_int("age_min_months"), age_max_months=read_int("age_max_months"),
        )
        flash("Potwierdzono aktualność karty.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )