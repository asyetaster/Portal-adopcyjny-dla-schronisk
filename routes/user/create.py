from flask import Flask, flash, redirect, url_for

from operations.user.CreateUserCommand import CreateUserCommand
from routes.user import read_user_name
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users")
    @page("admin/users/list.html", write=True)
    def add_user(create_user: CreateUserCommand):
        name = read_user_name("name")
        user_id = create_user.execute(name)
        flash("Utworzono użytkownika.")
        # Post/Redirect/Get: @page robi commit i zwraca przekierowanie bez renderowania.
        return redirect(url_for("user_details", user_id=user_id), code=303)