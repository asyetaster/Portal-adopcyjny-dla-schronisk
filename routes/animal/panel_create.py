from flask import Flask, flash, g, redirect, request, url_for

from auth import shelter_required
from operations.animal.CreateAnimalProfileCommand import CreateAnimalProfileCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals")
    @shelter_required(write=True)
    @page("panel/animals/new.html", write=True)
    def panel_animal_create(shelter_id: int, create: CreateAnimalProfileCommand):
        animal_id = create.execute(
            actor_id=g.user["id"],
            shelter_id=shelter_id,
            name=request.form.get("name", ""),
            species=request.form.get("species", ""),
        )
        flash("Utworzono szkic karty. Uzupełnij dane i dodaj zdjęcie.")
        return redirect(
            url_for("panel_animal_edit", shelter_id=shelter_id, animal_id=animal_id), code=303
        )