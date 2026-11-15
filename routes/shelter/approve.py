from flask import Flask, flash, g, redirect, url_for

from auth import admin_required
from operations.shelter.ApproveShelterRegistrationCommand import ApproveShelterRegistrationCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/shelters/<int:shelter_id>/approve")
    @admin_required
    @page("admin/shelters/details.html", write=True)
    def admin_shelter_approve(shelter_id: int, command: ApproveShelterRegistrationCommand):
        command.execute(actor_id=g.user["id"], shelter_id=shelter_id)
        flash("Placówka została zatwierdzona.")
        return redirect(url_for("admin_shelter_details", shelter_id=shelter_id), code=303)
