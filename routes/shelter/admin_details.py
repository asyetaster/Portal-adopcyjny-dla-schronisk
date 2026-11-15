from flask import Flask, abort

from auth import admin_required
from operations.shelter.GetShelterAdminQuery import GetShelterAdminQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/shelters/<int:shelter_id>")
    @admin_required
    @page("admin/shelters/details.html")
    def admin_shelter_details(shelter_id: int, get_shelter: GetShelterAdminQuery):
        shelter = get_shelter.execute(shelter_id)
        if shelter is None:
            abort(404)
        return {"shelter": shelter}
