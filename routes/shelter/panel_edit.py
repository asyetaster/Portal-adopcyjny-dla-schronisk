from flask import Flask

from auth import shelter_required
from operations.shelter import VOIVODESHIPS
from operations.shelter.GetShelterForManagementQuery import GetShelterForManagementQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/profile")
    @shelter_required()
    @page("panel/shelter/edit.html")
    def panel_shelter_edit(shelter_id: int, get_shelter: GetShelterForManagementQuery):
        return {"shelter": get_shelter.execute(shelter_id), "voivodeships": VOIVODESHIPS}
