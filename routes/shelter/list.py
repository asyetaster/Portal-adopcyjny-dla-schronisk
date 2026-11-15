from flask import Flask, request

from operations.shelter import VOIVODESHIPS
from operations.shelter.SearchSheltersQuery import SearchSheltersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/shelters")
    @page("shelters/list.html")
    def shelter_list(search_shelters: SearchSheltersQuery):
        name = request.args.get("name", "").strip()
        city = request.args.get("city", "").strip()
        voivodeship = request.args.get("voivodeship", "")
        if voivodeship not in VOIVODESHIPS:
            voivodeship = ""
        page_num = max(request.args.get("page", 1, type=int), 1)

        result = search_shelters.execute(
            name=name, voivodeship=voivodeship, city=city, page=page_num
        )
        return {
            "shelters": result["items"],
            "pagination": result["pagination"],
            "voivodeships": VOIVODESHIPS,
            "name": name,
            "city": city,
            "voivodeship": voivodeship,
        }
