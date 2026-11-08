from flask import Flask, flash, g, redirect, request, url_for

from auth import admin_required
from operations.user.BlockUserCommand import BlockUserCommand
from web import page


def register(app: Flask) -> None:
    @app.post("/admin/users/<int:user_id>/block")
    @admin_required
    @page("admin/users/details.html", write=True)
    def user_block(user_id: int, block_user: BlockUserCommand):
        block_user.execute(
            actor_id=g.user["id"],
            user_id=user_id,
            reason=request.form.get("reason", ""),
        )

        flash("Konto zostało zablokowane.")
        return redirect(url_for("user_details", user_id=user_id), code=303)
