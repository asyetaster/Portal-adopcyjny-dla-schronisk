"""Strona główna: wyszukiwarka i najnowsze karty zwierząt."""

from flask import Flask

from labels import LABELS
from operations.animal.SearchAnimalsQuery import SearchAnimalsQuery
from web import page

LATEST_ANIMALS = 8


def register(app: Flask) -> None:
    @app.get("/")
    @page("home.html")
    def home(search_animals: SearchAnimalsQuery):
        latest = search_animals.execute(sort="published", limit=LATEST_ANIMALS)
        return {"animals": latest["items"], "species_labels": LABELS["species"]}