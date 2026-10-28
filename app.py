"""Aplikacja Flask. Uruchomienie: flask --app app run

Trasy są w pakiecie routes/ (pogrupowane w podkatalogach, np. routes/user/)
i rejestrowane automatycznie.
"""

import os
import secrets
import warnings

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from database import create_engine_from_url, get_database_url
from routes import register_routes

csrf = CSRFProtect()


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["DATABASE_URL"] = get_database_url()
    if config:
        app.config.update(config)

    if not app.config["SECRET_KEY"]:
        warnings.warn(
            "Brak SECRET_KEY w środowisku - używam losowego klucza "
            "(sesje i tokeny CSRF przestaną działać po restarcie).",
            stacklevel=2,
        )
        app.config["SECRET_KEY"] = secrets.token_hex(32)

    csrf.init_app(app)
    # Engine tworzony raz na aplikację; połączenia otwiera @page na czas requestu.
    app.extensions["db_engine"] = create_engine_from_url(app.config["DATABASE_URL"])

    register_routes(app)
    return app