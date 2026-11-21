from flask import Flask, flash, g, redirect, url_for

from auth import admin_required
from operations.animal.UnhideAnimalProfileCommand import UnhideAnimalProfileCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/animals/<int:animal_id>/unhide")
    @admin_required
    @page("admin/animals/list.html", write=True)
    def admin_animal_unhide(animal_id: int, unhide: UnhideAnimalProfileCommand):
        unhide.execute(actor_id=g.user["id"], animal_id=animal_id)
        flash("Karta wróciła do katalogu.")
        return redirect(url_for("admin_animal_list"), code=303)