from flask import Flask, flash, g, redirect, url_for

from auth import login_required
from operations.user.UpdateMyProfileCommand import UpdateMyProfileCommand
from routes.user import read_profile_form
from web import page


def register(app: Flask) -> None:
    @app.post("/account/profile")
    @login_required
    @page("account/profile.html", write=True)
    def account_profile_update(update_profile: UpdateMyProfileCommand):
        data = read_profile_form()
        update_profile.execute(g.user["id"], **data)

        flash("Zapisano zmiany w profilu.")
        return redirect(url_for("account_profile"), code=303)
