from flask import Flask, request

from labels import LABELS
from operations.animal import SIZES, SPECIES
from operations.animal.SearchAnimalsQuery import SORTS, SearchAnimalsQuery
from operations.shelter import VOIVODESHIPS
from operations.shelter.GetShelterProfileQuery import GetShelterProfileQuery
from web import page


def _years(name: str) -> int | None:
    """Wiek z formularza w latach; niepoprawna wartość = brak filtra."""
    value = request.args.get(name, type=int)
    return value if value is not None and 0 <= value <= 50 else None


def register(app: Flask) -> None:
    @app.get("/animals")
    @page("animals/list.html")
    def animal_list(search_animals: SearchAnimalsQuery, get_shelter: GetShelterProfileQuery):
        # Filtry z adresu: wartości spoza list są po cichu pomijane.
        values = {
            "text": request.args.get("text", "").strip(),
            "species": request.args.get("species", ""),
            "sex": request.args.get("sex", ""),
            "sizes": [s for s in request.args.getlist("size") if s in SIZES],
            "voivodeship": request.args.get("voivodeship", ""),
            "city": request.args.get("city", "").strip(),
            "age_from": _years("age_from"),
            "age_to": _years("age_to"),
            "in_progress": request.args.get("in_progress") == "1",
            "sort": request.args.get("sort", "published"),
        }
        if values["species"] not in SPECIES:
            values["species"] = ""
        if values["sex"] not in ("Male", "Female"):
            values["sex"] = ""
        if values["voivodeship"] not in VOIVODESHIPS:
            values["voivodeship"] = ""
        if values["sort"] not in SORTS:
            values["sort"] = "published"

        shelter = None
        shelter_id = request.args.get("shelter_id", 0, type=int)
        if shelter_id > 0:
            shelter = get_shelter.execute(shelter_id)  # None, gdy niezatwierdzona

        page_num = max(request.args.get("page", 1, type=int), 1)
        result = search_animals.execute(
            text=values["text"],
            shelter_id=shelter["id"] if shelter else 0,
            species=values["species"],
            sex=values["sex"],
            sizes=",".join(values["sizes"]),
            voivodeship=values["voivodeship"],
            city=values["city"],
            # „Do 6 lat” obejmuje zwierzę, które skończyło 6 lat (do 6 lat i 11 miesięcy).
            age_from_months=values["age_from"] * 12 if values["age_from"] is not None else -1,
            age_to_months=values["age_to"] * 12 + 11 if values["age_to"] is not None else -1,
            include_in_progress=values["in_progress"],
            sort=values["sort"],
            page=page_num,
        )

        # Parametry do linków paginacji i „Wyczyść filtry” (bez wartości domyślnych).
        url_args = {
            "text": values["text"], "species": values["species"], "sex": values["sex"],
            "size": values["sizes"], "voivodeship": values["voivodeship"], "city": values["city"],
            "age_from": values["age_from"], "age_to": values["age_to"],
            "in_progress": "1" if values["in_progress"] else "",
            "sort": values["sort"] if values["sort"] != "published" else "",
            "shelter_id": shelter["id"] if shelter else "",
        }
        url_args = {k: v for k, v in url_args.items() if v not in ("", [], None)}
        filter_args = {k: v for k, v in url_args.items() if k != "shelter_id"}

        return {
            "animals": result["items"],
            "pagination": result["pagination"],
            "values": values,
            "url_args": url_args,
            "has_filters": bool(filter_args),
            "shelter": shelter,
            "voivodeships": VOIVODESHIPS,
            "species_labels": LABELS["species"],
            "sex_labels": LABELS["sex"],
            "size_labels": LABELS["size"],
        }