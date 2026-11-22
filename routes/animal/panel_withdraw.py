from flask import Flask, flash, g, redirect, request, url_for

from auth import shelter_required
from operations.animal.WithdrawAnimalProfileCommand import WithdrawAnimalProfileCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/withdraw")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_withdraw(shelter_id: int, animal_id: int, withdraw: WithdrawAnimalProfileCommand):
        withdraw.execute(
            actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id,
            reason=request.form.get("reason", ""),
        )
        flash("Karta wycofana z katalogu.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )