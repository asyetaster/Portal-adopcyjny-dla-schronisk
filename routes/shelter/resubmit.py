from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.shelter.ResubmitShelterRegistrationCommand import (
    ResubmitShelterRegistrationCommand,
)
from routes.shelter import read_shelter_form
from web import page


def register(app: Flask) -> None:
    @app.post("/account/shelters/<int:shelter_id>/resubmit")
    @shelter_required(manager=True)
    @page("account/shelters/form.html", write=True)
    def shelter_resubmit(shelter_id: int, resubmit: ResubmitShelterRegistrationCommand):
        resubmit.execute(actor_id=g.user["id"], shelter_id=shelter_id, **read_shelter_form())
        flash("Zgłoszenie zostało wysłane ponownie.")
        return redirect(url_for("my_shelters"), code=303)
