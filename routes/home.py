"""Tymczasowa strona główna. Docelowy widok (katalog zwierząt) powstaje w M3."""

from flask import Flask

from web import page


def register(app: Flask) -> None:
    @app.get("/")
    @page("home.html")
    def home():
        return {}
