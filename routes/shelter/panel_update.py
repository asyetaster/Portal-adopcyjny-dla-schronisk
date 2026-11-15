from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.shelter.UpdateShelterProfileCommand import UpdateShelterProfileCommand
from routes.shelter import read_shelter_form
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/profile")
    @shelter_required(write=True)
    @page("panel/shelter/edit.html", write=True)
    def panel_shelter_update(shelter_id: int, update: UpdateShelterProfileCommand):
        update.execute(actor_id=g.user["id"], shelter_id=shelter_id, **read_shelter_form())
        flash("Zapisano profil placówki.")
        return redirect(url_for("panel_shelter_edit", shelter_id=shelter_id), code=303)
