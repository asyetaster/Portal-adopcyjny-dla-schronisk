from flask import Flask, flash, g, redirect, url_for

from auth import shelter_required
from operations.shelter.RemoveShelterEmployeeCommand import RemoveShelterEmployeeCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/employees/<int:user_id>/remove")
    @shelter_required(manager=True, write=True)
    @page("panel/employees/list.html", write=True)
    def panel_employee_remove(
        shelter_id: int, user_id: int, remove: RemoveShelterEmployeeCommand
    ):
        remove.execute(actor_id=g.user["id"], shelter_id=shelter_id, user_id=user_id)
        flash("Usunięto pracownika.")
        if user_id == g.user["id"]:
            return redirect(url_for("my_shelters"), code=303)
        return redirect(url_for("panel_employees", shelter_id=shelter_id), code=303)
