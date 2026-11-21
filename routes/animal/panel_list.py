from flask import Flask, request

from auth import shelter_required
from labels import LABELS
from operations.animal import SPECIES
from operations.animal.ListShelterAnimalsQuery import SORTS, ListShelterAnimalsQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/animals")
    @shelter_required()
    @page("panel/animals/list.html")
    def panel_animal_list(shelter_id: int, list_animals: ListShelterAnimalsQuery):
        text = request.args.get("text", "").strip()
        status = request.args.get("status", "")
        if status not in LABELS["animal"]:
            status = ""
        species = request.args.get("species", "")
        if species not in SPECIES:
            species = ""
        sort = request.args.get("sort", "updated")
        if sort not in SORTS:
            sort = "updated"
        page_num = max(request.args.get("page", 1, type=int), 1)

        result = list_animals.execute(
            shelter_id=shelter_id, text=text, status=status,
            species=species, sort=sort, page=page_num,
        )
        return {
            "animals": result["items"],
            "pagination": result["pagination"],
            "text": text, "status": status, "species": species, "sort": sort,
            "status_labels": LABELS["animal"],
            "species_labels": LABELS["species"],
        }