from flask import Flask, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from operations.user.CreateUserCommand import CreateUserCommand
from routes.user import handle_user_integrity_error, read_user_form
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users")
    @page("admin/users/list.html", write=True)
    def add_user(create_user: CreateUserCommand):
        data = read_user_form(creating=True)

        try:
            user_id = create_user.execute(**data)
        except IntegrityError as error:
            handle_user_integrity_error(error)

        flash("Utworzono użytkownika.")

        return redirect(
            url_for("user_details", user_id=user_id),
            code=303,
        )