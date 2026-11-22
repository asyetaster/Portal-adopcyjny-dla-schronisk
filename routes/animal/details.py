from flask import Flask, abort, g

from operations.animal.GetAnimalProfileQuery import GetAnimalProfileQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/animals/<int:animal_id>")
    @page("animals/details.html")
    def animal_details(animal_id: int, get_animal: GetAnimalProfileQuery):
        animal = get_animal.execute(animal_id, viewer_id=g.user["id"] if g.user else 0)
        if animal is None:
            abort(404)  # szkic, wycofana, ukryta i adoptowana wyglądają jak nieistniejące
        return {"animal": animal}