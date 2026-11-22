from flask import Flask, abort

from operations.animal.SearchAnimalsQuery import SearchAnimalsQuery
from operations.shelter.GetShelterProfileQuery import GetShelterProfileQuery
from web import page

ANIMALS_ON_PROFILE = 8


def register(app: Flask) -> None:
    @app.get("/shelters/<int:shelter_id>")
    @page("shelters/details.html")
    def shelter_details(
        shelter_id: int,
        get_profile: GetShelterProfileQuery,
        search_animals: SearchAnimalsQuery,
    ):
        shelter = get_profile.execute(shelter_id)
        if shelter is None:
            abort(404)
        # BR-017: ta sama wyszukiwarka, ograniczona do placówki.
        animals = search_animals.execute(shelter_id=shelter_id, limit=ANIMALS_ON_PROFILE)
        return {
            "shelter": shelter,
            "animals": animals["items"],
            "animals_total": animals["pagination"]["total"],
        }