from flask import Flask, render_template

from auth import admin_required
from mailer import list_mails


def register(app: Flask) -> None:
    @app.get("/admin/mails")
    @admin_required
    def admin_mail_list():
        return render_template("admin/mails/list.html", mails=list_mails())
