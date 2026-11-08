"""Testy M1: rejestracja, profil, blokowanie, komendy konsolowe, filtr listy."""

import pytest
from sqlalchemy import text

from operations.errors import BusinessRuleError, NotFoundError
from operations.user.BlockUserCommand import BlockUserCommand
from operations.user.CreateUserCommand import CreateUserCommand
from operations.user.ListUsersQuery import ListUsersQuery
from operations.user.LoginUserQuery import LoginUserQuery
from operations.user.MakeAdminCommand import MakeAdminCommand
from operations.user.RegisterUserCommand import RegisterUserCommand
from operations.user.SetUserPasswordCommand import SetUserPasswordCommand
from operations.user.UnblockUserCommand import UnblockUserCommand


def _run(app, cls, **kwargs):
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        trans = conn.begin()
        result = cls(conn).execute(**kwargs)
        trans.commit()
    return result


def _user(app, email, *, is_admin=False, first_name="Jan", last_name="Kowalski"):
    return _run(
        app,
        CreateUserCommand,
        email=email,
        password="demo1234",
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin,
    )


def _login(client, email, password="demo1234"):
    return client.post("/login", data={"email": email, "password": password})


def _row(app, user_id):
    with app.extensions["db_engine"].connect() as conn:
        return conn.execute(
            text("SELECT * FROM users WHERE id = :id"), {"id": user_id}
        ).mappings().one()


REGISTER_DATA = {
    "email": "nowy@example.com",
    "password": "demo1234",
    "password_confirm": "demo1234",
    "first_name": "Anna",
    "last_name": "Nowak",
}


# --- Rejestracja ---------------------------------------------------------

def test_register_form_renders(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"password_confirm" in response.data


def test_register_without_phone_then_login(app, client):
    response = client.post("/register", data=REGISTER_DATA)
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/login")

    response = _login(client, "nowy@example.com")
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/")


def test_register_stores_null_phone_and_no_admin(app):
    user_id = _run(
        app, RegisterUserCommand,
        email="a@example.com", password="demo1234", first_name="A", last_name="B",
    )
    row = _row(app, user_id)
    assert row["phone"] is None
    assert row["is_admin"] == 0


def test_register_duplicate_email(app, client):
    _user(app, "nowy@example.com")
    response = client.post(
        "/register", data=REGISTER_DATA, headers={"Referer": "http://localhost/register"}
    )
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/register")
    with client.session_transaction() as sess:
        messages = [m for _, m in sess["_flashes"]]
    assert any("już istnieje" in m for m in messages)


def test_register_short_password(app):
    with pytest.raises(BusinessRuleError):
        _run(
            app, RegisterUserCommand,
            email="a@example.com", password="krotkie", first_name="A", last_name="B",
        )


def test_register_password_mismatch(client):
    response = client.post("/register", data={**REGISTER_DATA, "password_confirm": "inne1234"})
    assert response.status_code == 303
    with client.session_transaction() as sess:
        assert "Hasła nie są takie same." in [m for _, m in sess["_flashes"]]


# --- Profil --------------------------------------------------------------

def test_profile_requires_login(client):
    response = client.get("/account/profile")
    assert response.status_code == 302
    assert "/login?next=/account/profile" in response.headers["Location"]


def test_profile_update(app, client):
    user_id = _user(app, "jan@example.com")
    _login(client, "jan@example.com")

    response = client.get("/account/profile")
    assert response.status_code == 200
    assert b"jan@example.com" in response.data

    response = client.post("/account/profile", data={
        "first_name": "Janek", "last_name": "Nowy", "phone": "123456789",
        "email": "zmiana@example.com",  # ignorowane
    })
    assert response.status_code == 303
    row = _row(app, user_id)
    assert (row["first_name"], row["last_name"], row["phone"]) == ("Janek", "Nowy", "123456789")
    assert row["email"] == "jan@example.com"


# --- Blokowanie ----------------------------------------------------------

def test_block_requires_reason_and_not_self(app):
    admin_id = _user(app, "admin@example.com", is_admin=True)
    user_id = _user(app, "jan@example.com")
    with pytest.raises(BusinessRuleError):
        _run(app, BlockUserCommand, actor_id=admin_id, user_id=user_id, reason="  ")
    with pytest.raises(BusinessRuleError):
        _run(app, BlockUserCommand, actor_id=admin_id, user_id=admin_id, reason="test")
    with pytest.raises(NotFoundError):
        _run(app, BlockUserCommand, actor_id=admin_id, user_id=999, reason="test")


def test_block_logs_out_and_prevents_login(app, client):
    admin_id = _user(app, "admin@example.com", is_admin=True)
    user_id = _user(app, "jan@example.com")

    user_client = app.test_client()
    _login(user_client, "jan@example.com")
    assert user_client.get("/account/profile").status_code == 200

    _login(client, "admin@example.com")
    response = client.post(f"/admin/users/{user_id}/block", data={"reason": "Spam"})
    assert response.status_code == 303
    row = _row(app, user_id)
    assert row["status"] == "Blocked"
    assert row["blocked_by"] == admin_id
    assert row["blocked_reason"] == "Spam"

    # Sesja zablokowanego zostaje wyczyszczona przy następnym żądaniu.
    assert user_client.get("/account/profile").status_code == 302
    response = user_client.post(
        "/login",
        data={"email": "jan@example.com", "password": "demo1234"},
        headers={"Referer": "http://localhost/login"},
    )
    assert response.status_code == 303
    assert response.headers["Location"].endswith("/login")
    with user_client.session_transaction() as sess:
        assert "user_id" not in sess
        messages = [m for _, m in sess["_flashes"]]
    assert any("zablokowane" in m for m in messages)
    assert not any("Niepoprawny" in m for m in messages)

    response = client.post(f"/admin/users/{user_id}/unblock")
    assert response.status_code == 303
    row = _row(app, user_id)
    assert row["status"] == "Active"
    assert row["blocked_reason"] is None
    assert _login(user_client, "jan@example.com").status_code == 303


def test_unblock_active_user_fails(app):
    admin_id = _user(app, "admin@example.com", is_admin=True)
    user_id = _user(app, "jan@example.com")
    with pytest.raises(BusinessRuleError):
        _run(app, UnblockUserCommand, actor_id=admin_id, user_id=user_id)


def test_block_forbidden_for_regular_user(app, client):
    _user(app, "jan@example.com")
    other_id = _user(app, "ola@example.com")
    _login(client, "jan@example.com")
    response = client.post(f"/admin/users/{other_id}/block", data={"reason": "x"})
    assert response.status_code == 403
    assert _row(app, other_id)["status"] == "Active"


# --- Komendy konsolowe ---------------------------------------------------

def test_make_admin_gives_access(app, client):
    _user(app, "jan@example.com")
    _login(client, "jan@example.com")
    assert client.get("/admin/users").status_code == 403

    _run(app, MakeAdminCommand, email="jan@example.com")
    assert client.get("/admin/users").status_code == 200

    with pytest.raises(NotFoundError):
        _run(app, MakeAdminCommand, email="brak@example.com")


def test_set_user_password(app):
    _user(app, "jan@example.com")
    _run(app, SetUserPasswordCommand, email="jan@example.com", password="nowehaslo")
    with app.extensions["db_engine"].connect() as conn:
        login = LoginUserQuery(conn)
        assert login.execute(email="jan@example.com", password="demo1234") is None
        assert login.execute(email="jan@example.com", password="nowehaslo") is not None
    with pytest.raises(BusinessRuleError):
        _run(app, SetUserPasswordCommand, email="jan@example.com", password="krotkie")


# --- Lista z filtrem -----------------------------------------------------

def test_list_users_search_and_status(app):
    admin_id = _user(app, "admin@example.com", is_admin=True, first_name="Admin", last_name="Root")
    _user(app, "jan@example.com", first_name="Jan")
    ola_id = _user(app, "ola@example.com", first_name="Ola", last_name="Zielińska")
    _run(app, BlockUserCommand, actor_id=admin_id, user_id=ola_id, reason="test")

    with app.extensions["db_engine"].connect() as conn:
        q = ListUsersQuery(conn)
        assert [u["email"] for u in q.execute(search="jan")["items"]] == ["jan@example.com"]
        assert [u["email"] for u in q.execute(search="Zieli")["items"]] == ["ola@example.com"]
        blocked = q.execute(status="Blocked")
        assert blocked["pagination"]["total"] == 1
        assert q.execute(search="%")["pagination"]["total"] == 0


def test_list_users_filter_route(app, client):
    _user(app, "admin@example.com", is_admin=True, first_name="Admin", last_name="Root")
    _user(app, "jan@example.com")
    _login(client, "admin@example.com")
    response = client.get("/admin/users?search=jan&status=Active")
    assert response.status_code == 200
    assert b"jan@example.com" in response.data
    assert b"admin@example.com</td>" not in response.data
