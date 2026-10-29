from flask import Flask, abort, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from operations.user.GetUserQuery import GetUserQuery
from operations.user.UpdateUserCommand import UpdateUserCommand
from routes.user import handle_user_integrity_error, read_user_form
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users/<int:user_id>")
    @page("admin/users/details.html", write=True)
    def update_user(
        user_id: int,
        update_user: UpdateUserCommand,
        get_user: GetUserQuery,
    ):
        user = get_user.execute(user_id)

        if user is None:
            abort(404)

        if user["status"] == "Anonymized":
            abort(
                409,
                description="Nie można edytować zanonimizowanego konta",
            )

        data = read_user_form(creating=False)

        try:
            update_user.execute(user_id, **data)
        except IntegrityError as error:
            handle_user_integrity_error(error)

        flash("Zaktualizowano użytkownika.")

        return redirect(
            url_for("user_details", user_id=user_id),
            code=303,
        )