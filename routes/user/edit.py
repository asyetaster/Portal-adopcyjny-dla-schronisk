from flask import Flask, abort

from operations.user.GetUserQuery import GetUserQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users/<int:user_id>/edit")
    @page("admin/users/edit.html")
    def user_edit(user_id: int, get_user: GetUserQuery):
        # Formularz edycji wypełniony bieżącymi danymi;
        # zapis obsługuje update_user (POST /admin/users/<user_id>).
        user = get_user.execute(user_id)
        if user is None:
            abort(404)
        return {"user": user}
