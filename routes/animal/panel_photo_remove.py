from flask import Flask, flash, redirect, url_for

from auth import shelter_required
from operations.animal.RemoveAnimalPhotoCommand import RemoveAnimalPhotoCommand
from routes.animal import delete_photo_file
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/photos/<int:photo_id>/remove")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_photo_remove(
        shelter_id: int, animal_id: int, photo_id: int, remove_photo: RemoveAnimalPhotoCommand
    ):
        file_path = remove_photo.execute(
            shelter_id=shelter_id, animal_id=animal_id, photo_id=photo_id
        )
        delete_photo_file(file_path)
        flash("Usunięto zdjęcie.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )