from flask import Flask, flash, redirect, url_for

from auth import shelter_required
from operations.animal.SetMainAnimalPhotoCommand import SetMainAnimalPhotoCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/photos/<int:photo_id>/main")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_photo_main(
        shelter_id: int, animal_id: int, photo_id: int, set_main: SetMainAnimalPhotoCommand
    ):
        set_main.execute(shelter_id=shelter_id, animal_id=animal_id, photo_id=photo_id)
        flash("Zmieniono zdjęcie główne.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )