"""Kolejka e-maili.

``queue_mail(to, subject, template, **ctx)``:
- w requeście: wiadomość trafia do kolejki w ``g``; wysyła ją dopiero
  ``after_request`` (``routes/mail.py``), i to tylko przy odpowiedzi < 400,
  czyli po commicie transakcji,
- poza requestem (``test.py``): wysyłka od razu.

Bez ``MAIL_SERVER`` w środowisku wiadomość jest dopisywana do
``instance/mails.log`` (zmiana ścieżki: ``MAIL_LOG_PATH``). Z ``MAIL_SERVER``
idzie przez SMTP (opcjonalnie: ``MAIL_PORT``, ``MAIL_USERNAME``,
``MAIL_PASSWORD``, ``MAIL_FROM``, ``MAIL_USE_TLS`` = 1/0).

Szablony tekstowe leżą w ``templates/mail/`` (np. ``mail/welcome.txt``).
"""

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import g, has_request_context
from jinja2 import Environment, FileSystemLoader

from operations.common import now_utc

BASE_DIR = Path(__file__).resolve().parent
QUEUE_KEY = "mail_queue"

# Własne środowisko Jinja, żeby mailer działał też bez aplikacji Flask (test.py).
_templates = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=False,  # wiadomości tekstowe
    keep_trailing_newline=True,
)


def queue_mail(to: str, subject: str, template: str, **ctx) -> None:
    for value in (to, subject):
        if "\n" in value or "\r" in value:
            raise ValueError("Adresat i temat nie mogą zawierać znaków nowej linii")

    # Renderujemy od razu: błąd szablonu ma przerwać request (rollback).
    body = _templates.get_template(template).render(**ctx)
    message = {"to": to, "subject": subject, "body": body}

    if has_request_context():
        g.setdefault(QUEUE_KEY, []).append(message)
    else:
        send_mail(message)


def pop_queued_mails() -> list[dict]:
    """Zwraca i czyści kolejkę bieżącego requestu."""
    return g.pop(QUEUE_KEY, [])


def discard_queued_mails() -> None:
    g.pop(QUEUE_KEY, None)


def send_mail(message: dict) -> None:
    server = os.environ.get("MAIL_SERVER")
    if server:
        _send_smtp(server, message)
    else:
        _write_log(message)


def _write_log(message: dict) -> None:
    path = Path(os.environ.get("MAIL_LOG_PATH") or BASE_DIR / "instance" / "mails.log")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log:
        log.write(
            f"=== {now_utc()} ===\n"
            f"To: {message['to']}\n"
            f"Subject: {message['subject']}\n\n"
            f"{message['body']}\n"
        )


def _send_smtp(server: str, message: dict) -> None:
    email = EmailMessage()
    email["From"] = os.environ.get("MAIL_FROM", "portal@localhost")
    email["To"] = message["to"]
    email["Subject"] = message["subject"]
    email.set_content(message["body"])

    with smtplib.SMTP(server, int(os.environ.get("MAIL_PORT", "587")), timeout=10) as smtp:
        if os.environ.get("MAIL_USE_TLS", "1") == "1":
            smtp.starttls()
        username = os.environ.get("MAIL_USERNAME")
        if username:
            smtp.login(username, os.environ.get("MAIL_PASSWORD", ""))
        smtp.send_message(email)
