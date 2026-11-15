from flask import Flask, g

from auth import login_required
from operations.shelter import SHELTER_STATUS_LABELS
from operations.shelter.ListMySheltersQuery import ListMySheltersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/account/shelters")
    @login_required
    @page("account/shelters/list.html")
    def my_shelters(list_my_shelters: ListMySheltersQuery):
        return {
            "shelters": list_my_shelters.execute(g.user["id"]),
            "status_labels": SHELTER_STATUS_LABELS,
        }
