from flask import Flask, flash, g, redirect, request, url_for

from auth import shelter_required
from operations.shelter.AssignShelterEmployeeCommand import AssignShelterEmployeeCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/panel/shelters/<int:shelter_id>/employees")
    @shelter_required(manager=True, write=True)
    @page("panel/employees/list.html", write=True)
    def panel_employee_assign(shelter_id: int, assign: AssignShelterEmployeeCommand):
        assign.execute(
            actor_id=g.user["id"],
            shelter_id=shelter_id,
            email=request.form.get("email", ""),
            is_manager=request.form.get("is_manager") == "1",
        )
        flash("Dodano pracownika.")
        return redirect(url_for("panel_employees", shelter_id=shelter_id), code=303)
