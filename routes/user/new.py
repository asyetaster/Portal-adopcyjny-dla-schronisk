from flask import Flask

from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users/new")
    @page("admin/users/new.html")
    def user_new():
        # Czysta strona z formularzem; zapis obsługuje add_user (POST /admin/users).
        return {}
