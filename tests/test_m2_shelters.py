"""Testy M2: zgłoszenie i zatwierdzanie placówek, katalog, panel, personel, blokada."""

import pytest
from sqlalchemy import text

from mailer import list_mails, read_mail
from operations.errors import BusinessRuleError
from operations.shelter.ApproveShelterRegistrationCommand import (
    ApproveShelterRegistrationCommand,
)
from operations.shelter.AssignShelterEmployeeCommand import AssignShelterEmployeeCommand
from operations.shelter.BlockShelterCommand import BlockShelterCommand
from operations.shelter.RejectShelterRegistrationCommand import (
    RejectShelterRegistrationCommand,
)
from operations.shelter.RemoveShelterEmployeeCommand import RemoveShelterEmployeeCommand
from operations.shelter.ResubmitShelterRegistrationCommand import (
    ResubmitShelterRegistrationCommand,
)
from operations.shelter.SearchSheltersQuery import SearchSheltersQuery
from operations.shelter.SubmitShelterRegistrationCommand import (
    SubmitShelterRegistrationCommand,
)
from operations.shelter.UnblockShelterCommand import UnblockShelterCommand
from operations.demo.SeedDemoDataCommand import SHELTERS, SeedDemoDataCommand
from operations.user.BlockUserCommand import BlockUserCommand
from operations.user.CreateUserCommand import CreateUserCommand


def _run(app, cls, **kwargs):
    with app.app_context():
        engine = app.extensions["db_engine"]
        with engine.connect() as conn:
            trans = conn.begin()
            result = cls(conn).execute(**kwargs)
            trans.commit()
    return result


def _user(app, email, *, is_admin=False):
    return _run(
        app,
        CreateUserCommand,
        email=email,
        password="demo1234",
        first_name="Jan",
        last_name=email.split("@")[0],
        is_admin=is_admin,
    )


def _login(client, email):
    return client.post("/login", data={"email": email, "password": "demo1234"})


def _shelter_data(**overrides):
    data = {
        "name": "Schronisko Testowe",
        "street_address": "ul. Testowa 1",
        "postal_code": "00-001",
        "city": "Warszawa",
        "voivodeship": "mazowieckie",
        "contact_email": "kontakt@schronisko.example",
    }
    data.update(overrides)
    return data


def _submit(app, actor_id, **overrides):
    return _run(app, SubmitShelterRegistrationCommand, actor_id=actor_id, **_shelter_data(**overrides))


def _shelter(app, shelter_id):
    with app.extensions["db_engine"].connect() as conn:
        return conn.execute(
            text("SELECT * FROM shelters WHERE id = :id"), {"id": shelter_id}
        ).mappings().one()


def _mails(app):
    """Treść wszystkich zapisanych maili (nagłówki + body) jako jeden tekst."""
    with app.app_context():
        return "\n".join(
            f"{m['to']} {m['subject']} {read_mail(m['name'])['body']}" for m in list_mails()
        )


@pytest.fixture()
def world(app):
    """Admin, kierownicy dwóch zatwierdzonych placówek A i B, zwykły użytkownik."""
    admin = _user(app, "admin@example.com", is_admin=True)
    manager_a = _user(app, "a@example.com")
    manager_b = _user(app, "b@example.com")
    user = _user(app, "user@example.com")
    shelter_a = _submit(app, manager_a, name="Schronisko A")
    shelter_b = _submit(app, manager_b, name="Schronisko B", city="Kraków", voivodeship="małopolskie")
    for sid in (shelter_a, shelter_b):
        _run(app, ApproveShelterRegistrationCommand, actor_id=admin, shelter_id=sid)
    return {
        "admin": admin, "manager_a": manager_a, "manager_b": manager_b, "user": user,
        "shelter_a": shelter_a, "shelter_b": shelter_b,
    }


# --- Zgłoszenie → zatwierdzenie → katalog -------------------------------

def test_full_registration_flow(app, client):
    _user(app, "admin@example.com", is_admin=True)
    _user(app, "owner@example.com")

    _login(client, "owner@example.com")
    resp = client.post("/account/shelters", data=_shelter_data(name="Nowe Schronisko"))
    assert resp.status_code == 303
    assert "Nowe Schronisko" in client.get("/account/shelters").get_data(as_text=True)
    assert "Nowe Schronisko" not in client.get("/shelters").get_data(as_text=True)

    shelter_id = 1
    assert _shelter(app, shelter_id)["status"] == "Pending"
    # Panel działa dla Pending (R3) i pokazuje baner.
    panel = client.get(f"/panel/shelters/{shelter_id}")
    assert panel.status_code == 200
    assert "oczekuje na zatwierdzenie" in panel.get_data(as_text=True)
    client.post("/logout")

    _login(client, "admin@example.com")
    assert "Nowe Schronisko" in client.get("/admin/shelters/pending").get_data(as_text=True)
    resp = client.post(f"/admin/shelters/{shelter_id}/approve")
    assert resp.status_code == 303
    assert _shelter(app, shelter_id)["status"] == "Approved"
    assert "owner@example.com" in _mails(app)

    assert "Nowe Schronisko" in client.get("/shelters").get_data(as_text=True)
    assert client.get(f"/shelters/{shelter_id}").status_code == 200


def test_submitter_becomes_manager(app):
    owner = _user(app, "owner@example.com")
    sid = _submit(app, owner)
    with app.extensions["db_engine"].connect() as conn:
        row = conn.execute(
            text("SELECT is_manager FROM shelter_employees WHERE shelter_id=:s AND user_id=:u"),
            {"s": sid, "u": owner},
        ).one()
    assert row.is_manager == 1


def test_invalid_voivodeship_rejected(app):
    owner = _user(app, "owner@example.com")
    with pytest.raises(BusinessRuleError):
        _submit(app, owner, voivodeship="Bawaria")


def test_reject_and_resubmit(app):
    admin = _user(app, "admin@example.com", is_admin=True)
    owner = _user(app, "owner@example.com")
    sid = _submit(app, owner)

    with pytest.raises(BusinessRuleError):
        _run(app, RejectShelterRegistrationCommand, actor_id=admin, shelter_id=sid, reason=" ")
    _run(app, RejectShelterRegistrationCommand, actor_id=admin, shelter_id=sid, reason="Brak danych")
    row = _shelter(app, sid)
    assert row["status"] == "Rejected" and row["rejection_reason"] == "Brak danych"
    assert "Brak danych" in _mails(app)

    _run(app, ResubmitShelterRegistrationCommand, actor_id=owner, shelter_id=sid,
         **_shelter_data(name="Poprawiona nazwa"))
    row = _shelter(app, sid)
    assert row["status"] == "Pending"
    assert row["rejection_reason"] is None and row["decided_at"] is None
    assert row["name"] == "Poprawiona nazwa"

    with pytest.raises(BusinessRuleError):  # tylko z Rejected
        _run(app, ResubmitShelterRegistrationCommand, actor_id=owner, shelter_id=sid, **_shelter_data())


def test_approve_only_pending(app, world):
    with pytest.raises(BusinessRuleError):
        _run(app, ApproveShelterRegistrationCommand, actor_id=world["admin"], shelter_id=world["shelter_a"])


def test_no_mail_when_action_fails(app, client, world):
    _login(client, "admin@example.com")
    before = _mails(app)
    client.post(f"/admin/shelters/{world['shelter_a']}/approve")  # już Approved → błąd
    assert _mails(app) == before


# --- Wyszukiwanie (BR-014) ------------------------------------------------

def test_search_filters(app, world):
    owner = _user(app, "c@example.com")
    _submit(app, owner, name="Schronisko Pending")  # niezatwierdzone

    def names(**kw):
        return {s["name"] for s in _run(app, SearchSheltersQuery, **kw)["items"]}

    assert names() == {"Schronisko A", "Schronisko B"}
    assert names(name="ko a") == {"Schronisko A"}
    assert names(name="Schronisko A") == {"Schronisko A"}
    assert names(voivodeship="małopolskie") == {"Schronisko B"}
    assert names(city="krak") == {"Schronisko B"}
    assert names(name="Pending") == set()


def test_blocked_shelter_hidden_from_catalog(app, client, world):
    _run(app, BlockShelterCommand, actor_id=world["admin"], shelter_id=world["shelter_a"], reason="Nadużycia")
    assert "Schronisko A" not in client.get("/shelters").get_data(as_text=True)
    assert client.get(f"/shelters/{world['shelter_a']}").status_code == 404


# --- Uprawnienia (AC-005) -------------------------------------------------

def test_employee_cannot_access_other_shelter(app, client, world):
    b = world["shelter_b"]
    _login(client, "a@example.com")
    assert client.get(f"/panel/shelters/{world['shelter_a']}").status_code == 200
    assert client.get(f"/panel/shelters/{b}").status_code == 403
    assert client.get(f"/panel/shelters/{b}/profile").status_code == 403
    assert client.get(f"/panel/shelters/{b}/employees").status_code == 403
    resp = client.post(f"/panel/shelters/{b}/profile", data=_shelter_data(name="Przejęte"))
    assert resp.status_code == 403
    assert _shelter(app, b)["name"] == "Schronisko B"
    resp = client.post(f"/panel/shelters/{b}/employees", data={"email": "user@example.com"})
    assert resp.status_code == 403


def test_panel_requires_login_and_employment(client, world):
    resp = client.get(f"/panel/shelters/{world['shelter_a']}")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]
    _login(client, "user@example.com")
    assert client.get(f"/panel/shelters/{world['shelter_a']}").status_code == 403


def test_admin_routes_forbidden_for_employee(client, world):
    _login(client, "a@example.com")
    assert client.get("/admin/shelters").status_code == 403
    assert client.post(f"/admin/shelters/{world['shelter_b']}/block", data={"reason": "x"}).status_code == 403


def test_update_profile_via_panel(app, client, world):
    _login(client, "a@example.com")
    resp = client.post(
        f"/panel/shelters/{world['shelter_a']}/profile",
        data=_shelter_data(name="Schronisko A+", contact_phone="123"),
    )
    assert resp.status_code == 303
    row = _shelter(app, world["shelter_a"])
    assert row["name"] == "Schronisko A+" and row["contact_phone"] == "123"


# --- Personel -------------------------------------------------------------

def test_manager_assigns_and_removes_employee(app, client, world):
    sid = world["shelter_a"]
    _login(client, "a@example.com")
    resp = client.post(f"/panel/shelters/{sid}/employees", data={"email": "USER@example.com"})
    assert resp.status_code == 303
    assert "user@example.com" in client.get(f"/panel/shelters/{sid}/employees").get_data(as_text=True)

    resp = client.post(f"/panel/shelters/{sid}/employees/{world['user']}/remove")
    assert resp.status_code == 303
    assert "user@example.com" not in client.get(f"/panel/shelters/{sid}/employees").get_data(as_text=True)


def test_non_manager_cannot_manage_staff(app, client, world):
    sid = world["shelter_a"]
    _run(app, AssignShelterEmployeeCommand, actor_id=world["manager_a"], shelter_id=sid, email="user@example.com")
    _login(client, "user@example.com")
    assert client.get(f"/panel/shelters/{sid}/employees").status_code == 200
    assert client.post(f"/panel/shelters/{sid}/employees", data={"email": "b@example.com"}).status_code == 403
    assert client.post(f"/panel/shelters/{sid}/employees/{world['manager_a']}/remove").status_code == 403


def test_assign_requires_active_account(app, world):
    _run(app, BlockUserCommand, actor_id=world["admin"], user_id=world["user"], reason="spam")
    with pytest.raises(BusinessRuleError):
        _run(app, AssignShelterEmployeeCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], email="user@example.com")
    with pytest.raises(BusinessRuleError):
        _run(app, AssignShelterEmployeeCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], email="nikt@example.com")


def test_assign_duplicate_rejected(app, world):
    with pytest.raises(BusinessRuleError):
        _run(app, AssignShelterEmployeeCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], email="a@example.com")


def test_cannot_remove_last_manager(app, world):
    sid = world["shelter_a"]
    with pytest.raises(BusinessRuleError):
        _run(app, RemoveShelterEmployeeCommand, actor_id=world["manager_a"], shelter_id=sid, user_id=world["manager_a"])

    _run(app, AssignShelterEmployeeCommand, actor_id=world["manager_a"], shelter_id=sid,
         email="user@example.com", is_manager=True)
    _run(app, RemoveShelterEmployeeCommand, actor_id=world["manager_a"], shelter_id=sid, user_id=world["manager_a"])


# --- Blokada (R5) ---------------------------------------------------------

def test_blocked_shelter_panel_read_only(app, client, world):
    sid = world["shelter_a"]
    _run(app, BlockShelterCommand, actor_id=world["admin"], shelter_id=sid, reason="Kontrola")
    _login(client, "a@example.com")
    page = client.get(f"/panel/shelters/{sid}")
    assert page.status_code == 200 and "tylko do odczytu" in page.get_data(as_text=True)
    assert client.post(f"/panel/shelters/{sid}/profile", data=_shelter_data()).status_code == 403
    assert client.post(f"/panel/shelters/{sid}/employees", data={"email": "user@example.com"}).status_code == 403


def test_unblock_restores_previous_status(app, world):
    admin = world["admin"]
    approved = world["shelter_a"]
    pending = _submit(app, world["user"], name="Oczekujące")

    for sid in (approved, pending):
        _run(app, BlockShelterCommand, actor_id=admin, shelter_id=sid, reason="Kontrola")
        assert _shelter(app, sid)["status"] == "Blocked"
        _run(app, UnblockShelterCommand, actor_id=admin, shelter_id=sid)

    assert _shelter(app, approved)["status"] == "Approved"
    assert _shelter(app, pending)["status"] == "Pending"
    assert _shelter(app, approved)["blocked_reason"] is None


def test_admin_pages_render(client, world):
    _login(client, "admin@example.com")
    assert client.get("/admin/shelters").status_code == 200
    assert client.get("/admin/shelters?status=Approved&search=A").status_code == 200
    assert client.get("/admin/shelters/pending").status_code == 200
    assert client.get(f"/admin/shelters/{world['shelter_a']}").status_code == 200
    assert client.get("/admin/shelters/999").status_code == 404


# --- Dane demo ------------------------------------------------------------

def test_seed_demo_data_is_idempotent(app):
    first = _run(app, SeedDemoDataCommand)
    second = _run(app, SeedDemoDataCommand)
    assert first["shelters"] == len(SHELTERS) and second["shelters"] == 0
    # Katalog publiczny: tylko zatwierdzone (BR-014). "items" to jedna strona,
    # więc liczymy po "total" z paginacji.
    approved = sum(1 for _, _, status, _ in SHELTERS if status == "Approved")
    assert _run(app, SearchSheltersQuery)["pagination"]["total"] == approved
