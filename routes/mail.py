"""Zapis maili zebranych przez ``mailer.queue_mail`` (pliki .eml) po udanym requeście."""

from flask import Flask, g

from mailer import flush_queued_mails


def register(app: Flask) -> None:
    @app.after_request
    def send_queued_mails(response):
        if response.status_code < 400:
            flush_queued_mails()
        else:
            g.pop("_mails", None)  # transakcja wycofana — maile przepadają
        return response
