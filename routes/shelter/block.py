from flask import Flask, flash, g, redirect, request, url_for

from auth import admin_required
from operations.shelter.BlockShelterCommand import BlockShelterCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/shelters/<int:shelter_id>/block")
    @admin_required
    @page("admin/shelters/details.html", write=True)
    def admin_shelter_block(shelter_id: int, command: BlockShelterCommand):
        command.execute(actor_id=g.user["id"], shelter_id=shelter_id, reason=request.form.get("reason", ""))
        flash("Placówka została zablokowana.")
        return redirect(url_for("admin_shelter_details", shelter_id=shelter_id), code=303)
