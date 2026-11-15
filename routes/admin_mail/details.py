from flask import Flask, abort, render_template, send_file

from auth import admin_required
from mailer import read_mail


def register(app: Flask) -> None:
    @app.get("/admin/mails/<name>")
    @admin_required
    def admin_mail_details(name: str):
        mail = read_mail(name)
        if mail is None:
            abort(404)
        return render_template("admin/mails/details.html", mail=mail)

    @app.get("/admin/mails/<name>/download")
    @admin_required
    def admin_mail_download(name: str):
        mail = read_mail(name)
        if mail is None:
            abort(404)
        return send_file(
            mail["path"],
            mimetype="message/rfc822",
            as_attachment=True,
            download_name=name,
        )
