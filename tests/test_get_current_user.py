from operations.user.CreateUserCommand import CreateUserCommand
from operations.user.GetCurrentUserQuery import GetCurrentUserQuery


def _create_user(app, **kwargs) -> int:
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        trans = conn.begin()
        user_id = CreateUserCommand(conn).execute(**kwargs)
        trans.commit()
    return user_id


def test_get_current_user_existing(app):
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
        result = GetCurrentUserQuery(conn).execute(user_id)

    assert result is not None
    assert result["id"] == user_id
    assert result["first_name"] == "Admin"
    assert result["is_admin"] == 1
    assert result["status"] == "Active"


def test_get_current_user_nonexistent(app):
    engine = app.extensions["db_engine"]
    with engine.connect() as conn:
        result = GetCurrentUserQuery(conn).execute(99999)

    assert result is None
