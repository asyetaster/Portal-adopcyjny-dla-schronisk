import pytest
from flask import g
from werkzeug.exceptions import Forbidden

from auth import is_safe_redirect_url, require_admin_access
from operations.user.CreateUserCommand import CreateUserCommand


# ---------------------------------------------------------------------------
# Helper: tworzenie użytkownika w bazie testowej (osobne połączenie + commit)
# ---------------------------------------------------------------------------

def _create_user(app, **kwargs) -> int:
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        trans = conn.begin()
        user_id = CreateUserCommand(conn).execute(**kwargs)
        trans.commit()
    return user_id


# ---------------------------------------------------------------------------
# Testy jednostkowe: auth.require_admin_access / is_safe_redirect_url
# ---------------------------------------------------------------------------

def test_require_admin_unauthenticated_redirects(app):
    with app.test_request_context("/admin/users"):
        g.user = None
        response = require_admin_access()
        assert response is not None
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]
        assert "next=/admin/users" in response.headers["Location"]


def test_require_admin_non_admin_forbidden(app):
    with app.test_request_context("/admin/users"):
        g.user = {"id": 1, "first_name": "X", "is_admin": 0, "status": "Active"}
        with pytest.raises(Forbidden):
            require_admin_access()


def test_require_admin_admin_passes(app):
    with app.test_request_context("/admin/users"):
        g.user = {"id": 1, "first_name": "X", "is_admin": 1, "status": "Active"}
        assert require_admin_access() is None


def test_require_admin_non_admin_path_passes(app):
    with app.test_request_context("/login"):
        g.user = None
        assert require_admin_access() is None


def test_is_safe_redirect_url_accepts_relative():
    assert is_safe_redirect_url("/admin/users")
    assert is_safe_redirect_url("/")


def test_is_safe_redirect_url_rejects_external():
    assert not is_safe_redirect_url("//evil.com")
    assert not is_safe_redirect_url("https://evil.com")
    assert not is_safe_redirect_url("http://evil.com")


def test_is_safe_redirect_url_rejects_empty():
    assert not is_safe_redirect_url("")


# ---------------------------------------------------------------------------
# Testy tras: logowanie, wylogowanie, ochrona /admin
# ---------------------------------------------------------------------------

def test_admin_protected_redirects_to_login(client):
    """NieZalogowany dostęp do /admin/users → przekierowanie na /login."""
    response = client.get("/admin/users")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
    assert "next=/admin/users" in response.headers["Location"]


def test_login_form_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"E-mail" in response.data
    assert b"password" in response.data


def test_login_wrong_password(app, client):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )

    response = client.post("/login", data={
        "email": "admin@example.com",
        "password": "wrong",
    })
    assert response.status_code == 200  # re-render form
    assert b"Niepoprawny" in response.data

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_login_correct_admin(app, client):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )

    response = client.post("/login", data={
        "email": "admin@example.com",
        "password": "demo1234",
        "next": "/admin/users",
    })
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/admin/users")

    with client.session_transaction() as sess:
        assert sess["user_id"] is not None


def test_admin_accessible_after_login(app, client):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )
    client.post("/login", data={
        "email": "admin@example.com",
        "password": "demo1234",
    })

    response = client.get("/admin/users")
    assert response.status_code == 200


def test_logout_clears_session(app, client):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )
    client.post("/login", data={
        "email": "admin@example.com",
        "password": "demo1234",
    })

    response = client.post("/logout")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_open_redirect_blocked(app, client):
    """next=https://evil.com → fallback na domyślny cel, nie na zewnętrzny URL."""
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )

    response = client.post("/login", data={
        "email": "admin@example.com",
        "password": "demo1234",
        "next": "https://evil.com",
    })
    assert response.status_code == 303
    assert "evil.com" not in response.headers["Location"]
    assert response.headers["Location"].endswith("/admin/users")


# ---------------------------------------------------------------------------
# Test integracyjny: pełny przepływ logowania i ochrony /admin
# ---------------------------------------------------------------------------

def test_integration_admin_and_non_admin_flow(app, client):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )
    _create_user(
        app,
        email="user@example.com",
        password="demo1234",
        first_name="Regular",
        last_name="User",
        is_admin=False,
    )

    # 1. Anonimowy dostęp do /admin → przekierowanie na logowanie
    response = client.get("/admin/users")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    # 2. Logowanie jako admin → dostęp do /admin/users
    response = client.post("/login", data={
        "email": "admin@example.com",
        "password": "demo1234",
    })
    assert response.status_code == 303
    response = client.get("/admin/users")
    assert response.status_code == 200

    # 3. Wylogowanie
    response = client.post("/logout")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    # 4. Logowanie jako zwykły użytkownik → 403 na /admin/users
    response = client.post("/login", data={
        "email": "user@example.com",
        "password": "demo1234",
    })
    assert response.status_code == 303
    response = client.get("/admin/users")
    assert response.status_code == 403
    assert b"Wyloguj" in response.data
    assert b"/logout" in response.data
