from flask import Flask, abort, g

from auth import shelter_required
from operations.shelter import VOIVODESHIPS
from operations.shelter.GetShelterForManagementQuery import GetShelterForManagementQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/account/shelters/<int:shelter_id>/resubmit")
    @shelter_required(manager=True)
    @page("account/shelters/form.html")
    def shelter_resubmit_form(shelter_id: int, get_shelter: GetShelterForManagementQuery):
        if g.shelter["status"] != "Rejected":
            abort(404)
        shelter = get_shelter.execute(shelter_id)
        return {"shelter": shelter, "voivodeships": VOIVODESHIPS, "resubmit": True}
