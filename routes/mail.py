"""Wysyłka e-maili z kolejki po zakończeniu requestu (patrz mailer.py)."""

from flask import Flask, current_app
from werkzeug.wrappers import Response

from mailer import pop_queued_mails, send_mail


def register(app: Flask) -> None:
    @app.after_request
    def send_queued_mails(response: Response) -> Response:
        messages = pop_queued_mails()

        # Odpowiedź >= 400 => transakcja została wycofana, więc nic nie wysyłamy.
        if response.status_code < 400:
            for message in messages:
                try:
                    send_mail(message)
                except Exception:
                    # Błąd wysyłki nie może zepsuć już zatwierdzonej operacji.
                    current_app.logger.exception(
                        "Nie udało się wysłać e-maila do %s", message["to"]
                    )

        return response
