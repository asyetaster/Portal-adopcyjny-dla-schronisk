"""Kolejka e-maili.

``queue_mail(to, subject, template, **ctx)``:

- w kontekście requestu dopisuje maila do kolejki w ``g``; ``routes/mail.py``
  wysyła ją w ``after_request`` tylko przy odpowiedzi < 400 (czyli po commicie),
  a przy wycofanej transakcji kolejkę czyści ``discard_queued_mails()``,
- poza requestem (``test.py``, testy operacji) wysyła od razu.

Sposób wysyłki (``send_mail``):

- z ``MAIL_SERVER`` w środowisku — SMTP (opcjonalnie: ``MAIL_PORT``,
  ``MAIL_USERNAME``, ``MAIL_PASSWORD``, ``MAIL_FROM``, ``MAIL_USE_TLS`` = 1/0),
- bez ``MAIL_SERVER`` — zapis jako plik ``.eml`` w ``instance/mails/``
  (ścieżkę nadpisuje ``MAIL_DIR`` z konfiguracji aplikacji albo ze środowiska).
  Pliki ``.eml`` otworzy każdy klient poczty, a administrator przegląda je
  w ``/admin/mails``.

Treść maila to szablon Jinja z ``templates/mails/``.
"""

import os
import re
import smtplib
import uuid
from datetime import datetime, timezone
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path

from flask import current_app, g, has_app_context, has_request_context
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MAIL_DIR = BASE_DIR / "instance" / "mails"
DEFAULT_MAIL_FROM = "Portal adopcyjny <no-reply@portal-adopcyjny.local>"
QUEUE_KEY = "mail_queue"

# Nazwy plików tworzy tylko save_mail(); ten wzorzec chroni przed
# odczytem spoza katalogu (np. "../app.db") w read_mail().
MAIL_FILE_PATTERN = re.compile(r"\d{8}T\d{6}\d{6}Z-[0-9a-f]{8}\.eml")

# Własne środowisko Jinja, żeby mailer działał też bez aplikacji Flask (test.py).
_env = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates" / "mails"),
    autoescape=False,  # wiadomości tekstowe
    keep_trailing_newline=True,
)


def mail_dir() -> Path:
    if has_app_context() and current_app.config.get("MAIL_DIR"):
        return Path(current_app.config["MAIL_DIR"])
    if os.environ.get("MAIL_DIR"):
        return Path(os.environ["MAIL_DIR"])
    return DEFAULT_MAIL_DIR


def queue_mail(to: str, subject: str, template: str, **ctx) -> None:
    for value in (to, subject):
        if "\n" in value or "\r" in value:
            raise ValueError("Adresat i temat nie mogą zawierać znaków nowej linii")

    # Renderujemy od razu: błąd szablonu ma przerwać request (rollback).
    mail = {
        "to": to,
        "subject": subject,
        "body": _env.get_template(template).render(**ctx),
    }
    if has_request_context():
        g.setdefault(QUEUE_KEY, []).append(mail)
    else:
        send_mail(mail)


def pop_queued_mails() -> list[dict]:
    """Zwraca i czyści kolejkę bieżącego requestu."""
    return g.pop(QUEUE_KEY, [])


def discard_queued_mails() -> None:
    """Transakcja wycofana — zakolejkowane maile przepadają."""
    g.pop(QUEUE_KEY, None)


def send_mail(mail: dict) -> None:
    server = os.environ.get("MAIL_SERVER")
    if server:
        _send_smtp(server, mail)
    else:
        save_mail(mail)


def _build_message(mail: dict, now: datetime) -> EmailMessage:
    message = EmailMessage()
    message["From"] = os.environ.get("MAIL_FROM", DEFAULT_MAIL_FROM)
    message["To"] = mail["to"]
    message["Subject"] = mail["subject"]
    message["Date"] = format_datetime(now)
    message.set_content(mail["body"])
    return message


def _send_smtp(server: str, mail: dict) -> None:
    message = _build_message(mail, datetime.now(timezone.utc))
    port = int(os.environ.get("MAIL_PORT", "587"))
    with smtplib.SMTP(server, port, timeout=10) as smtp:
        if os.environ.get("MAIL_USE_TLS", "1") == "1":
            smtp.starttls()
        username = os.environ.get("MAIL_USERNAME")
        if username:
            smtp.login(username, os.environ.get("MAIL_PASSWORD", ""))
        smtp.send_message(message)


def save_mail(mail: dict) -> Path:
    """Zapisuje maila jako ``<czas UTC>-<losowy sufiks>.eml``; zwraca ścieżkę."""
    now = datetime.now(timezone.utc)
    message = _build_message(mail, now)

    directory = mail_dir()
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{now.strftime('%Y%m%dT%H%M%S%f')}Z-{uuid.uuid4().hex[:8]}.eml"
    path = directory / name
    path.write_bytes(message.as_bytes(policy=policy.SMTP))
    return path


def _parse(path: Path):
    with path.open("rb") as file:
        return BytesParser(policy=policy.default).parse(file)


def list_mails() -> list[dict]:
    """Zapisane maile, najnowsze najpierw: name, to, subject, date (UTC ISO), size."""
    directory = mail_dir()
    if not directory.is_dir():
        return []
    mails = []
    for path in sorted(directory.glob("*.eml"), reverse=True):
        if not MAIL_FILE_PATTERN.fullmatch(path.name):
            continue
        message = _parse(path)
        mails.append({
            "name": path.name,
            "to": message["To"],
            "subject": message["Subject"],
            "date": _iso(message["Date"]),
            "size": path.stat().st_size,
        })
    return mails


def read_mail(name: str) -> dict | None:
    """Jeden mail po nazwie pliku (z nagłówkami, treścią i surowym .eml) albo None."""
    if not MAIL_FILE_PATTERN.fullmatch(name):
        return None
    path = mail_dir() / name
    if not path.is_file():
        return None
    message = _parse(path)
    body = message.get_body(preferencelist=("plain",))
    return {
        "name": name,
        "from": message["From"],
        "to": message["To"],
        "subject": message["Subject"],
        "date": _iso(message["Date"]),
        "body": body.get_content() if body is not None else "",
        "path": path,
    }


def _iso(value) -> str:
    try:
        return parsedate_to_datetime(str(value)).astimezone(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    except (TypeError, ValueError):
        return ""
