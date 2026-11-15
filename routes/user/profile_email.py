from flask import Flask, abort, flash, g, redirect, request, url_for

from auth import login_required
from operations.user import MAX_EMAIL_LENGTH
from operations.user.ChangeMyEmailCommand import ChangeMyEmailCommand
from routes.user import EMAIL_PATTERN, read_required_text
from web import page


def register(app: Flask) -> None:
    @app.post("/account/email")
    @login_required
    @page("account/profile.html", write=True)
    def account_email_update(change_email: ChangeMyEmailCommand):
        email = read_required_text("email", "E-mail", MAX_EMAIL_LENGTH)
        if not EMAIL_PATTERN.fullmatch(email):
            abort(400, description="Podaj poprawny adres e-mail")

        change_email.execute(
            g.user["id"],
            email=email,
            current_password=request.form.get("current_password", ""),
        )

        flash("Zmieniono adres e-mail.")
        return redirect(url_for("account_profile"), code=303)
