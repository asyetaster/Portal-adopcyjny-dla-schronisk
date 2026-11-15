"""Kolejka e-maili. Maile nie są wysyłane — każdy zapisujemy jako plik ``.eml``.

``queue_mail(to, subject, template, **ctx)``:

- w kontekście requestu dopisuje maila do ``g._mails``; ``routes/mail.py``
  zapisuje je w ``after_request`` tylko przy odpowiedzi < 400, a ``@page``
  czyści kolejkę przy wycofanej transakcji,
- poza requestem (``test.py``, testy operacji) zapisuje od razu.

Pliki trafiają do ``instance/mails/`` (ścieżkę można nadpisać przez
``MAIL_DIR`` w konfiguracji aplikacji). Pliki ``.eml`` otworzy każdy klient
poczty, a administrator przegląda je w ``/admin/mails``.
Treść maila to szablon Jinja z ``templates/mails/``.
"""

import re
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
MAIL_FROM = "Portal adopcyjny <no-reply@portal-adopcyjny.local>"

# Nazwy plików tworzy tylko save_mail(); ten wzorzec chroni przed
# odczytem spoza katalogu (np. "../app.db") w read_mail().
MAIL_FILE_PATTERN = re.compile(r"\d{8}T\d{6}\d{6}Z-[0-9a-f]{8}\.eml")

_env = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates" / "mails"),
    keep_trailing_newline=True,
)


def mail_dir() -> Path:
    if has_app_context() and current_app.config.get("MAIL_DIR"):
        return Path(current_app.config["MAIL_DIR"])
    return DEFAULT_MAIL_DIR


def queue_mail(to: str, subject: str, template: str, **ctx) -> None:
    mail = {
        "to": to,
        "subject": subject,
        "body": _env.get_template(template).render(**ctx),
    }
    if has_request_context():
        g.setdefault("_mails", []).append(mail)
    else:
        save_mail(mail)


def save_mail(mail: dict) -> Path:
    """Zapisuje maila jako ``<czas UTC>-<losowy sufiks>.eml``; zwraca ścieżkę."""
    now = datetime.now(timezone.utc)
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = mail["to"]
    message["Subject"] = mail["subject"]
    message["Date"] = format_datetime(now)
    message.set_content(mail["body"])

    directory = mail_dir()
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{now.strftime('%Y%m%dT%H%M%S%f')}Z-{uuid.uuid4().hex[:8]}.eml"
    path = directory / name
    path.write_bytes(message.as_bytes(policy=policy.SMTP))
    return path


def flush_queued_mails() -> None:
    """Zapisuje maile zebrane w ``g._mails`` i czyści kolejkę."""
    for mail in g.pop("_mails", []):
        save_mail(mail)


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
