from flask import Flask, flash, g, redirect, url_for

from auth import admin_required
from operations.user.UnblockUserCommand import UnblockUserCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users/<int:user_id>/unblock")
    @admin_required
    @page("admin/users/details.html", write=True)
    def user_unblock(user_id: int, unblock_user: UnblockUserCommand):
        unblock_user.execute(actor_id=g.user["id"], user_id=user_id)

        flash("Konto zostało odblokowane.")
        return redirect(url_for("user_details", user_id=user_id), code=303)
