"""Testy mailera (zapis .eml) i podglądu maili w panelu administracyjnym."""

from email import policy
from email.parser import BytesParser
from pathlib import Path

from mailer import list_mails, queue_mail, read_mail
from operations.user.CreateUserCommand import CreateUserCommand


def _user(app, email, *, is_admin=False):
    with app.extensions["db_engine"].connect() as conn:
        trans = conn.begin()
        CreateUserCommand(conn).execute(
            email=email, password="demo1234", first_name="Jan",
            last_name="Kowalski", is_admin=is_admin,
        )
        trans.commit()


def _login(client, email):
    client.post("/login", data={"email": email, "password": "demo1234"})


def _queue(app, to="ktos@example.com"):
    with app.app_context():
        queue_mail(to, "Zażółć gęślą jaźń", "shelter_rejected.txt",
                   first_name="Anna", shelter_name="Azyl", reason="Brak opisu")


def test_mail_saved_as_eml(app):
    _queue(app)
    files = list(Path(app.config["MAIL_DIR"]).glob("*.eml"))
    assert len(files) == 1
    message = BytesParser(policy=policy.default).parsebytes(files[0].read_bytes())
    assert message["To"] == "ktos@example.com"
    assert message["Subject"] == "Zażółć gęślą jaźń"
    assert "Brak opisu" in message.get_body(preferencelist=("plain",)).get_content()


def test_list_and_read(app):
    _queue(app, "a@example.com")
    _queue(app, "b@example.com")
    with app.app_context():
        mails = list_mails()
        assert [m["to"] for m in mails] == ["b@example.com", "a@example.com"]  # najnowsze najpierw
        assert read_mail(mails[0]["name"])["body"].startswith("Dzień dobry Anna")
        assert read_mail("../app.db") is None
        assert read_mail("nie-istnieje.eml") is None


def test_admin_mail_pages(app, client):
    _user(app, "admin@example.com", is_admin=True)
    _queue(app)
    _login(client, "admin@example.com")
    with app.app_context():
        name = list_mails()[0]["name"]

    page = client.get("/admin/mails").get_data(as_text=True)
    assert "ktos@example.com" in page and "Zażółć gęślą jaźń" in page

    details = client.get(f"/admin/mails/{name}")
    assert details.status_code == 200 and "Brak opisu" in details.get_data(as_text=True)

    download = client.get(f"/admin/mails/{name}/download")
    assert download.status_code == 200
    assert download.mimetype == "message/rfc822"
    assert b"Subject:" in download.data

    assert client.get("/admin/mails/..%2Fapp.db").status_code == 404
    assert client.get("/admin/mails/20990101T000000000000Z-deadbeef.eml").status_code == 404


def test_admin_mail_pages_require_admin(app, client):
    _user(app, "user@example.com")
    assert client.get("/admin/mails").status_code == 302  # niezalogowany → /login
    _login(client, "user@example.com")
    assert client.get("/admin/mails").status_code == 403


def test_empty_mail_list(app, client):
    _user(app, "admin@example.com", is_admin=True)
    _login(client, "admin@example.com")
    assert "Brak zapisanych maili" in client.get("/admin/mails").get_data(as_text=True)
