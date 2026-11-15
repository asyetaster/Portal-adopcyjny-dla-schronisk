from flask import Flask

from auth import login_required
from operations.shelter import VOIVODESHIPS
from web import page


def register(app: Flask) -> None:
    @app.get("/account/shelters/new")
    @login_required
    @page("account/shelters/form.html")
    def shelter_new():
        return {"shelter": {}, "voivodeships": VOIVODESHIPS, "resubmit": False}
