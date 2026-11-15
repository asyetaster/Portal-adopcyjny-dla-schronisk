"""Tworzenie Engine SQLAlchemy i inicjalizacja bazy SQLite."""

import os
from pathlib import Path

from sqlalchemy import Engine, create_engine, event

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def create_engine_from_url(url: str | None = None) -> Engine:
    """Tworzy Engine. Wywoływane raz na aplikację/proces."""
    engine = create_engine(url or get_database_url(), pool_pre_ping=True)
    if engine.dialect.name == "sqlite":
        _fix_sqlite_transactions(engine)
    return engine


def _fix_sqlite_transactions(engine: Engine) -> None:
    # Sterownik sqlite3 sam decyduje, kiedy wysłać BEGIN (dopiero przed DML).
    # Wyłączamy to i wysyłamy BEGIN sami, żeby transakcje SQLAlchemy
    # (commit/rollback) działały przewidywalnie. Przepis z dokumentacji SQLAlchemy.
    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_connection, connection_record):
        dbapi_connection.isolation_level = None
        # SQLite domyślnie ignoruje klucze obce; włączamy je dla każdego połączenia.
        dbapi_connection.execute("PRAGMA foreign_keys = ON")

    @event.listens_for(engine, "begin")
    def _on_begin(connection):
        # Command otwiera transakcję jako BEGIN IMMEDIATE (blokada zapisu od razu),
        # żeby dwa równoległe commandy nie czytały tego samego stanu (np. M7).
        # pop(): connection.info żyje razem z połączeniem w puli, więc flaga
        # musi działać tylko na jedną transakcję.
        immediate = connection.info.pop("begin_immediate", False)
        connection.exec_driver_sql("BEGIN IMMEDIATE" if immediate else "BEGIN")


def init_db(engine: Engine) -> None:
    """Wykonuje schema.sql (tabela users + użytkownik demonstracyjny)."""
    script = SCHEMA_PATH.read_text(encoding="utf-8")
    raw = engine.raw_connection()
    try:
        raw.driver_connection.executescript(script)
    finally:
        raw.close()


if __name__ == "__main__":
    engine = create_engine_from_url()
    init_db(engine)
    print(f"Baza gotowa: {engine.url}")