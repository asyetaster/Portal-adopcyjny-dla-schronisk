from flask import Flask, flash, g, redirect, url_for

from auth import login_required
from operations.shelter.SubmitShelterRegistrationCommand import (
    SubmitShelterRegistrationCommand,
)
from routes.shelter import read_shelter_form
from web import page


def register(app: Flask) -> None:
    @app.post("/account/shelters")
    @login_required
    @page("account/shelters/form.html", write=True)
    def shelter_create(submit: SubmitShelterRegistrationCommand):
        submit.execute(actor_id=g.user["id"], **read_shelter_form())
        flash("Zgłoszenie placówki zostało wysłane. Czeka na zatwierdzenie przez administratora.")
        return redirect(url_for("my_shelters"), code=303)
