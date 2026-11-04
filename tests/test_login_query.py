from sqlalchemy import text

from operations.user.CreateUserCommand import CreateUserCommand
from operations.user.LoginUserQuery import LoginUserQuery


def _create_user(app, **kwargs) -> int:
    """Tworzy użytkownika i commituje (osobne połączenie). Zwraca ID."""
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        trans = conn.begin()
        user_id = CreateUserCommand(conn).execute(**kwargs)
        trans.commit()
    return user_id


def test_login_correct_password(app):
    user_id = _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
        is_admin=True,
    )

    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        result = LoginUserQuery(conn).execute(email="admin@example.com", password="demo1234")

    assert result is not None
    assert result["id"] == user_id
    assert result["is_admin"] == 1
    assert result["email"] == "admin@example.com"
    assert result["status"] == "Active"
    assert "password_hash" not in result


def test_login_wrong_password(app):
    _create_user(
        app,
        email="admin@example.com",
        password="demo1234",
        first_name="Admin",
        last_name="Root",
    )

    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        result = LoginUserQuery(conn).execute(email="admin@example.com", password="wrong")

    assert result is None


def test_login_blocked_user(app):
    _create_user(
        app,
        email="blocked@example.com",
        password="demo1234",
        first_name="Blocked",
        last_name="User",
    )

    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(
            text(
                "UPDATE users SET status = 'Blocked', blocked_reason = 'test' "
                "WHERE email = :email"
            ),
            {"email": "blocked@example.com"},
        )
        trans.commit()

    with engine.connect() as conn:
        result = LoginUserQuery(conn).execute(email="blocked@example.com", password="demo1234")

    assert result is None


def test_login_nonexistent_user(app):
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        result = LoginUserQuery(conn).execute(email="nobody@example.com", password="x")

    assert result is None
