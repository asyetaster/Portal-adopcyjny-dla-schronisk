from flask import Flask, flash, g, redirect, request, url_for

from auth import admin_required
from operations.animal.HideAnimalProfileCommand import HideAnimalProfileCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/animals/<int:animal_id>/hide")
    @admin_required
    @page("admin/animals/list.html", write=True)
    def admin_animal_hide(animal_id: int, hide: HideAnimalProfileCommand):
        hide.execute(
            actor_id=g.user["id"], animal_id=animal_id, reason=request.form.get("reason", "")
        )
        flash("Karta została ukryta w katalogu.")
        return redirect(url_for("admin_animal_list"), code=303)