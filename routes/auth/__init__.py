"""Trasy autentykacji: logowanie, wylogowanie i before_request.

Funkcje ``load_logged_in_user()`` i ``require_admin_access()`` pochodzą z
``auth.py``. Rejestrowane są w tej kolejności (ładowanie użytkownika przed
sprawdzaniem uprawnień), aby odmowa nastąpiła zanim ``@page`` otworzy transakcję.
"""

from flask import Flask, flash, redirect, render_template, request, session, url_for

from auth import is_safe_redirect_url, load_logged_in_user, require_admin_access
from operations.user.LoginUserQuery import LoginUserQuery
from web import page


def register(app: Flask) -> None:
    app.before_request(load_logged_in_user)
    app.before_request(require_admin_access)

    @app.get("/login")
    @page("login.html")
    def login():
        # Czysta strona z formularzem; obsługa POST w login_submit.
        return {}

    @app.post("/login")
    @page("login.html")
    def login_submit(login_user: LoginUserQuery):
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = login_user.execute(email=email, password=password)

        if user is None:
            flash("Niepoprawny e-mail lub hasło.")
            return {}

        session.clear()
        session["user_id"] = user["id"]
        flash(f"Witaj, {user['first_name']}!")

        next_url = request.form.get("next", "")
        target = next_url if is_safe_redirect_url(next_url) else url_for("user_list")
        return redirect(target, code=303)

    @app.post("/logout")
    def logout():
        session.clear()
        flash("Wylogowano.")
        return redirect(url_for("login"))

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403
