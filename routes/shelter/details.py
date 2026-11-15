from flask import Flask, abort

from operations.shelter.GetShelterProfileQuery import GetShelterProfileQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/shelters/<int:shelter_id>")
    @page("shelters/details.html")
    def shelter_details(shelter_id: int, get_profile: GetShelterProfileQuery):
        shelter = get_profile.execute(shelter_id)
        if shelter is None:
            abort(404)
        return {"shelter": shelter}
