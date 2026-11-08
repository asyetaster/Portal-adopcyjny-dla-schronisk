from flask import Flask, g, redirect, url_for

from web import page


def register(app: Flask) -> None:
    @app.get("/register")
    @page("register.html")
    def register_form():
        if g.user is not None:
            return redirect(url_for("home"))
        return {}
