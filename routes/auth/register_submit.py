from flask import Flask, flash, redirect, url_for

from operations.user.RegisterUserCommand import RegisterUserCommand
from routes.user import read_register_form
from web import page


def register(app: Flask) -> None:
    @app.post("/register")
    @page("register.html", write=True)
    def register_submit(register_user: RegisterUserCommand):
        data = read_register_form()
        register_user.execute(**data)

        flash("Konto zostało założone. Możesz się zalogować.")
        return redirect(url_for("login"), code=303)
