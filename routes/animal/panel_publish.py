from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.animal.PublishAnimalProfileCommand import PublishAnimalProfileCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/publish")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_publish(shelter_id: int, animal_id: int, publish: PublishAnimalProfileCommand):
        publish.execute(actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id)
        flash("Karta opublikowana.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )