from flask import Flask, abort

from operations.user.GetUserQuery import GetUserQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users/<int:user_id>")
    @page("admin/users/details.html")
    def user_details(user_id: int, get_user: GetUserQuery):
        user = get_user.execute(user_id)
        if user is None:
            abort(404)
        return {"user": user}