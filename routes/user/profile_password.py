from flask import Flask, flash, g, redirect, request, url_for

from auth import login_required
from operations.errors import BusinessRuleError
from operations.user.ChangeMyPasswordCommand import ChangeMyPasswordCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/account/password")
    @login_required
    @page("account/profile.html", write=True)
    def account_password_update(change_password: ChangeMyPasswordCommand):
        # Nie usuwamy spacji z haseł.
        new_password = request.form.get("new_password", "")
        if new_password != request.form.get("new_password_confirm", ""):
            raise BusinessRuleError("Hasła nie są takie same.")

        change_password.execute(
            g.user["id"],
            current_password=request.form.get("current_password", ""),
            new_password=new_password,
        )

        flash("Zmieniono hasło.")
        return redirect(url_for("account_profile"), code=303)
