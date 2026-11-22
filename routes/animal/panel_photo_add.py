from flask import Flask, flash, g, redirect, request, url_for

from auth import shelter_required
from operations.animal.AddAnimalPhotoCommand import AddAnimalPhotoCommand
from routes.animal import delete_photo_file, save_photo
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/photos")
    @shelter_required(write=True)
    @page("panel/animals/details.html", write=True)
    def panel_animal_photo_add(shelter_id: int, animal_id: int, add_photo: AddAnimalPhotoCommand):
        path = save_photo(request.files.get("photo"))
        try:
            add_photo.execute(
                actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id,
                file_path=path, alt_text=request.form.get("alt_text", ""),
            )
        except BaseException:
            # Operacja odmówiła (albo padła): plik nie ma właściciela w bazie.
            delete_photo_file(path)
            raise
        flash("Dodano zdjęcie.")
        return redirect(
            url_for("panel_animal_details", shelter_id=shelter_id, animal_id=animal_id), code=303
        )