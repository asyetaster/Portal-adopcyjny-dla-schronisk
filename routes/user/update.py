from flask import Flask, abort, flash, redirect, url_for

from operations.user.GetUserQuery import GetUserQuery
from operations.user.UpdateUserCommand import UpdateUserCommand
from routes.user import read_user_name
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users/<int:user_id>")
    @page("admin/users/details.html", write=True)
    def update_user(
        user_id: int,
        update_user: UpdateUserCommand,
        get_user: GetUserQuery,
    ):
        new_name = read_user_name("name")
        if get_user.execute(user_id) is None:
            abort(404)
        update_user.execute(user_id, new_name)
        flash("Zmieniono nazwę użytkownika.")
        # Post/Redirect/Get: @page robi commit i zwraca przekierowanie bez renderowania.
        return redirect(url_for("user_details", user_id=user_id), code=303)