from flask import Flask

from auth import shelter_required
from labels import LABELS
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/animals/new")
    @shelter_required(write=True)
    @page("panel/animals/new.html")
    def panel_animal_new(shelter_id: int):
        return {"species_labels": LABELS["species"]}