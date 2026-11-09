"""Testy fundamentów M0: klucze obce, BEGIN IMMEDIATE, 404, etykiety, paginacja, e-maile, błędy."""

import re

import pytest
from sqlalchemy import event, text
from sqlalchemy.exc import IntegrityError

from labels import label
from mailer import queue_mail
from operations.common import now_utc
from operations.errors import BusinessRuleError, NotFoundError
from operations.pagination import build_pagination, paginate
from web import page


# ---------- baza danych ----------

def test_foreign_keys_are_enforced(app):
    engine = app.extensions["db_engine"]
    with engine.connect() as connection:
        transaction = connection.begin()
        with pytest.raises(IntegrityError):
            connection.execute(
                text(
                    "INSERT INTO shelter_employees (shelter_id, user_id, assigned_by) "
                    "VALUES (999, 999, 999)"
                )
            )
        transaction.rollback()


def test_begin_immediate_only_for_write_pages_and_flag_does_not_leak(app, client):
    @app.post("/_t/write")
    @page("home.html", write=True)
    def t_write():
        return {}

    engine = app.extensions["db_engine"]
    statements = []

    @event.listens_for(engine, "before_cursor_execute")
    def record(conn, cursor, statement, parameters, context, executemany):
        if statement.startswith("BEGIN"):
            statements.append(statement)

    client.post("/_t/write")

    # Połączenie otwarte poza @page (jak load_logged_in_user w before_request)
    # trafia na to samo połączenie z puli i nie może odziedziczyć flagi.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    assert statements == ["BEGIN IMMEDIATE", "BEGIN"]


# ---------- strony błędów ----------

def test_home_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Portal adopcyjny" in response.get_data(as_text=True)


def test_unknown_path_renders_404_page(client):
    response = client.get("/tego-nie-ma")
    assert response.status_code == 404
    assert "Nie znaleziono" in response.get_data(as_text=True)


# ---------- etykiety ----------

def test_label_known_value():
    assert label("InContact", "adoption") == "W kontakcie"


def test_label_experience_none_string_is_not_missing_value():
    assert label("None", "experience") == "Brak"


def test_label_missing_value_and_unknown_group():
    assert label(None, "adoption") == "—"
    assert label("Cokolwiek", "adoption") == "Cokolwiek"
    assert label("Dog", "nie_ma_takiej_grupy") == "Dog"


def test_label_filter_registered_in_jinja(app):
    rendered = app.jinja_env.from_string("{{ 'Dog'|label('species') }}").render()
    assert rendered == "Pies"


# ---------- czas ----------

def test_now_utc_format():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", now_utc())


# ---------- paginacja ----------

def test_build_pagination():
    assert build_pagination(page=2, limit=10, total=25) == {
        "page": 2,
        "limit": 10,
        "total": 25,
        "total_pages": 3,
        "has_next": True,
        "has_previous": True,
    }


def test_paginate_returns_items_and_pagination(app):
    engine = app.extensions["db_engine"]
    with engine.begin() as connection:
        for i in range(3):
            connection.execute(
                text(
                    "INSERT INTO users (email, password_hash, first_name, last_name) "
                    "VALUES (:email, 'x', 'Jan', 'Test')"
                ),
                {"email": f"user{i}@example.com"},
            )

    with engine.connect() as connection:
        result = paginate(
            connection,
            count_sql="SELECT COUNT(*) FROM users",
            items_sql="SELECT id, email FROM users ORDER BY id",
            page=2,
            limit=2,
        )

    assert [item["email"] for item in result["items"]] == ["user2@example.com"]
    assert result["pagination"]["total"] == 3
    assert result["pagination"]["total_pages"] == 2
    assert result["pagination"]["has_previous"] is True
    assert result["pagination"]["has_next"] is False


@pytest.mark.parametrize("page_number,limit", [(0, 10), (1, 0), (-1, 5)])
def test_paginate_rejects_bad_arguments(app, page_number, limit):
    with app.extensions["db_engine"].connect() as connection:
        with pytest.raises(ValueError):
            paginate(
                connection,
                count_sql="SELECT COUNT(*) FROM users",
                items_sql="SELECT id FROM users ORDER BY id",
                page=page_number,
                limit=limit,
            )


# ---------- e-maile ----------

@pytest.fixture()
def mail_log(tmp_path, monkeypatch):
    path = tmp_path / "mails.log"
    monkeypatch.setenv("MAIL_LOG_PATH", str(path))
    monkeypatch.delenv("MAIL_SERVER", raising=False)
    return path


def test_queue_mail_outside_request_sends_immediately(mail_log):
    queue_mail("ala@example.com", "Temat testowy", "mail/test.txt", name="Ala")

    content = mail_log.read_text(encoding="utf-8")
    assert "To: ala@example.com" in content
    assert "Subject: Temat testowy" in content
    assert "Cześć Ala," in content


def test_queue_mail_rejects_header_injection(mail_log):
    with pytest.raises(ValueError):
        queue_mail("ala@example.com", "Temat\nBcc: ktos@example.com", "mail/test.txt", name="Ala")


@pytest.fixture()
def flow_app(app):
    """Aplikacja z trasami testowymi (dodanymi przed pierwszym requestem)."""

    @app.post("/_t/ok")
    def t_ok():
        queue_mail("ok@example.com", "Mail po sukcesie", "mail/test.txt", name="Ok")
        return "ok"

    @app.post("/_t/abort")
    def t_abort():
        from flask import abort

        queue_mail("abort@example.com", "Mail po abort", "mail/test.txt", name="Abort")
        abort(400)

    @app.post("/_t/rule")
    def t_rule():
        queue_mail("rule@example.com", "Mail po błędzie reguły", "mail/test.txt", name="Rule")
        raise BusinessRuleError("Komunikat testowy")

    @app.get("/_t/missing")
    def t_missing():
        raise NotFoundError("Brak takiego zwierzęcia")

    return app


def test_mail_is_sent_after_successful_response(flow_app, mail_log):
    response = flow_app.test_client().post("/_t/ok")
    assert response.status_code == 200
    assert "Subject: Mail po sukcesie" in mail_log.read_text(encoding="utf-8")


def test_mail_is_not_sent_when_response_is_error(flow_app, mail_log):
    response = flow_app.test_client().post("/_t/abort")
    assert response.status_code == 400
    assert not mail_log.exists()


def test_business_rule_error_flashes_and_discards_mail(flow_app, mail_log):
    response = flow_app.test_client().post("/_t/rule", follow_redirects=True)

    assert response.status_code == 200
    assert "Komunikat testowy" in response.get_data(as_text=True)
    assert not mail_log.exists()


def test_business_rule_error_redirects_to_same_host_referrer(flow_app, mail_log):
    response = flow_app.test_client().post(
        "/_t/rule", headers={"Referer": "http://localhost/poprzednia"}
    )
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/poprzednia")


def test_business_rule_error_ignores_foreign_referrer(flow_app, mail_log):
    response = flow_app.test_client().post(
        "/_t/rule", headers={"Referer": "https://evil.example/phishing"}
    )
    assert response.status_code == 303
    assert "evil.example" not in response.headers["Location"]


def test_not_found_error_renders_404_with_message(flow_app):
    response = flow_app.test_client().get("/_t/missing")
    assert response.status_code == 404
    assert "Brak takiego zwierzęcia" in response.get_data(as_text=True)
