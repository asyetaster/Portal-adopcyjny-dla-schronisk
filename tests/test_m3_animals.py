"""Testy M3: karty zwierząt, katalog, aktualność, moderacja."""

import pytest
from sqlalchemy import text

from operations.animal.AddAnimalPhotoCommand import AddAnimalPhotoCommand
from operations.animal.ConfirmAnimalProfileAccuracyCommand import (
    ConfirmAnimalProfileAccuracyCommand,
)
from operations.animal.CreateAnimalProfileCommand import CreateAnimalProfileCommand
from operations.animal.GetAnimalProfileForManagementQuery import (
    GetAnimalProfileForManagementQuery,
)
from operations.animal.ListShelterAnimalsQuery import ListShelterAnimalsQuery
from operations.animal.PublishAnimalProfileCommand import PublishAnimalProfileCommand
from operations.animal.RemoveAnimalPhotoCommand import RemoveAnimalPhotoCommand
from operations.animal.SetMainAnimalPhotoCommand import SetMainAnimalPhotoCommand
from operations.animal.UpdateAnimalCareRequirementsCommand import (
    UpdateAnimalCareRequirementsCommand,
)
from operations.animal.UpdateAnimalProfileCommand import UpdateAnimalProfileCommand
from operations.animal.WithdrawAnimalProfileCommand import WithdrawAnimalProfileCommand
from operations.errors import BusinessRuleError, NotFoundError
from operations.shelter.ApproveShelterRegistrationCommand import (
    ApproveShelterRegistrationCommand,
)
from operations.shelter.BlockShelterCommand import BlockShelterCommand
from operations.shelter.SubmitShelterRegistrationCommand import (
    SubmitShelterRegistrationCommand,
)
from operations.user.CreateUserCommand import CreateUserCommand


def _run(app, cls, **kwargs):
    """Jedna transakcja na wywołanie, jak w runnerze test.py."""
    with app.app_context():
        with app.extensions["db_engine"].connect() as conn:
            trans = conn.begin()
            try:
                result = cls(conn).execute(**kwargs)
            except BaseException:
                trans.rollback()
                raise
            trans.commit()
    return result


def _sql(app, query, **params):
    with app.extensions["db_engine"].connect() as conn:
        trans = conn.begin()
        result = conn.execute(text(query), params)
        rows = result.mappings().all() if result.returns_rows else []
        trans.commit()
    return rows


def _user(app, email, *, is_admin=False):
    return _run(
        app, CreateUserCommand, email=email, password="demo1234",
        first_name="Jan", last_name=email.split("@")[0], is_admin=is_admin,
    )


def _login(client, email):
    return client.post("/login", data={"email": email, "password": "demo1234"})


def _shelter(app, owner, name, *, approve_by=None, city="Warszawa", voivodeship="mazowieckie"):
    sid = _run(
        app, SubmitShelterRegistrationCommand, actor_id=owner, name=name,
        street_address="ul. Testowa 1", postal_code="00-001", city=city,
        voivodeship=voivodeship, contact_email="kontakt@example.com",
    )
    if approve_by:
        _run(app, ApproveShelterRegistrationCommand, actor_id=approve_by, shelter_id=sid)
    return sid


def _animal(app, actor, shelter_id, name="Burek", species="Dog", **profile):
    """Szkic z kompletnym profilem. Zdjęcia dodają testy z kolejnych commitów."""
    animal_id = _run(
        app, CreateAnimalProfileCommand, actor_id=actor, shelter_id=shelter_id,
        name=name, species=species,
    )
    data = dict(
        sex="Male", description="Spokojny pies.", daily_needs="Dwa spacery dziennie.",
        breed="Mieszaniec", size="Medium", age_min_months=24, age_max_months=36,
        temperament="łagodny, towarzyski",
    )
    data.update(profile)
    _run(
        app, UpdateAnimalProfileCommand, actor_id=actor, shelter_id=shelter_id,
        animal_id=animal_id, name=data.pop("name", name), species=species, **data,
    )
    return animal_id

def _photo(app, actor, shelter_id, animal_id, name="a.jpg"):
    return _run(app, AddAnimalPhotoCommand, actor_id=actor, shelter_id=shelter_id,
                animal_id=animal_id, file_path=f"uploads/animals/{name}", alt_text="Zdjęcie")


def _photos(app, animal_id):
    return _sql(app, "SELECT * FROM animal_photos WHERE animal_id = :id ORDER BY position", id=animal_id)

def _row(app, animal_id):
    return _sql(app, "SELECT * FROM animals WHERE id = :id", id=animal_id)[0]


@pytest.fixture()
def world(app):
    """Admin, kierownicy zatwierdzonych placówek A i B, placówka C (Pending), zwykły użytkownik."""
    admin = _user(app, "admin@example.com", is_admin=True)
    manager_a = _user(app, "a@example.com")
    manager_b = _user(app, "b@example.com")
    manager_c = _user(app, "c@example.com")
    user = _user(app, "user@example.com")
    return {
        "admin": admin, "manager_a": manager_a, "manager_b": manager_b,
        "manager_c": manager_c, "user": user,
        "shelter_a": _shelter(app, manager_a, "Schronisko A", approve_by=admin),
        "shelter_b": _shelter(
            app, manager_b, "Schronisko B", approve_by=admin,
            city="Bydgoszcz", voivodeship="kujawsko-pomorskie",
        ),
        "shelter_c": _shelter(app, manager_c, "Schronisko C"),  # Pending
    }


# --- Szkic, edycja, wymagania -------------------------------------------

def test_create_draft_also_for_pending_shelter(app, world):
    animal_id = _run(
        app, CreateAnimalProfileCommand, actor_id=world["manager_c"],
        shelter_id=world["shelter_c"], name="  Reksio ", species="Dog",
    )
    row = _row(app, animal_id)
    assert (row["status"], row["name"], row["published_at"]) == ("Draft", "Reksio", None)


def test_create_rejects_bad_input(app, world):
    for kwargs in ({"name": " ", "species": "Dog"}, {"name": "X", "species": "Rabbit"}):
        with pytest.raises(BusinessRuleError):
            _run(app, CreateAnimalProfileCommand, actor_id=world["manager_a"],
                 shelter_id=world["shelter_a"], **kwargs)


def test_blocked_shelter_cannot_create_cards(app, world):
    _run(app, BlockShelterCommand, actor_id=world["admin"],
         shelter_id=world["shelter_a"], reason="Test")
    with pytest.raises(BusinessRuleError, match="zablokowana"):
        _run(app, CreateAnimalProfileCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], name="Burek", species="Dog")


def test_update_profile_normalizes_values(app, world):
    animal_id = _animal(app, world["manager_a"], world["shelter_a"],
                        age_min_months=-1, age_max_months=18, temperament=" a , A,, b ")
    row = _row(app, animal_id)
    # Jedna granica wieku = wiek dokładny; tagi bez duplikatów i pustych.
    assert (row["age_min_months"], row["age_max_months"]) == (18, 18)
    assert row["temperament"] == "a,b"


def test_update_validates_age_and_species_change(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    common = dict(actor_id=actor, shelter_id=sid, animal_id=animal_id, name="Burek",
                  sex="Male", description="x", daily_needs="y")
    with pytest.raises(BusinessRuleError, match="dolna granica"):
        _run(app, UpdateAnimalProfileCommand, species="Dog",
             age_min_months=60, age_max_months=12, **common)
    # W szkicu gatunek wolno zmienić.
    _run(app, UpdateAnimalProfileCommand, species="Cat", **common)
    assert _row(app, animal_id)["species"] == "Cat"


def test_update_does_not_touch_confirmation(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    _sql(app, "UPDATE animals SET last_confirmed_at = '2026-01-01T00:00:00Z' WHERE id = :id",
         id=animal_id)
    _animal_update = dict(actor_id=actor, shelter_id=sid, animal_id=animal_id, name="Nowe",
                          species="Dog", sex="Male", description="Zmiana", daily_needs="y")
    _run(app, UpdateAnimalProfileCommand, **_animal_update)
    assert _row(app, animal_id)["last_confirmed_at"] == "2026-01-01T00:00:00Z"  # BR-044


def test_requirements_upsert_keeps_unknown_distinct_from_no(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    args = dict(actor_id=actor, shelter_id=sid, animal_id=animal_id,
                good_with_children="No", good_with_dogs="Unknown", good_with_cats="Yes",
                special_care_required="Unknown")
    _run(app, UpdateAnimalCareRequirementsCommand, activity_level="High", **args)
    _run(app, UpdateAnimalCareRequirementsCommand, activity_level="", **args)  # drugi zapis = update
    rows = _sql(app, "SELECT * FROM animal_care_requirements WHERE animal_id = :id", id=animal_id)
    assert len(rows) == 1
    assert (rows[0]["good_with_children"], rows[0]["good_with_dogs"]) == ("No", "Unknown")
    assert rows[0]["activity_level"] is None
    with pytest.raises(BusinessRuleError):
        _run(app, UpdateAnimalCareRequirementsCommand, **{**args, "good_with_cats": "Maybe"})


# --- Zakres placówki (BR-049, AC-005) -----------------------------------

def test_commands_are_scoped_to_shelter(app, world):
    animal_b = _animal(app, world["manager_b"], world["shelter_b"])
    with pytest.raises(NotFoundError):
        _run(app, UpdateAnimalProfileCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], animal_id=animal_b, name="Hak", species="Dog",
             sex="Male", description="x", daily_needs="y")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        assert GetAnimalProfileForManagementQuery(conn).execute(world["shelter_a"], animal_b) is None
        assert GetAnimalProfileForManagementQuery(conn).execute(world["shelter_b"], animal_b)


def test_management_query_lists_missing_fields(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _run(app, CreateAnimalProfileCommand, actor_id=actor, shelter_id=sid,
                     name="Pusty", species="Cat")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        animal = GetAnimalProfileForManagementQuery(conn).execute(sid, animal_id)
    assert animal["missing"] == [
        "opis charakteru", "codzienne potrzeby", "wiek lub przedział wieku",
        "wielkość", "co najmniej jedno zdjęcie",
    ]


def test_shelter_list_includes_drafts_and_filters(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    _animal(app, actor, sid, name="Burek")
    _animal(app, actor, sid, name="Mruczek", species="Cat")
    _animal(app, world["manager_b"], world["shelter_b"], name="Obcy")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        query = ListShelterAnimalsQuery(conn)
        names = [a["name"] for a in query.execute(sid, sort="name")["items"]]
        assert names == ["Burek", "Mruczek"]
        assert [a["name"] for a in query.execute(sid, species="Cat")["items"]] == ["Mruczek"]
        assert query.execute(sid, text="bur")["pagination"]["total"] == 1
        assert query.execute(sid, status="Available")["items"] == []



# --- Zdjęcia -------------------------------------------------------------

def test_first_photo_is_main_and_main_can_change(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    first = _photo(app, actor, sid, animal_id, "1.jpg")
    second = _photo(app, actor, sid, animal_id, "2.jpg")
    assert [(p["id"], p["is_main"], p["position"]) for p in _photos(app, animal_id)] == [
        (first, 1, 0), (second, 0, 1)]

    _run(app, SetMainAnimalPhotoCommand, shelter_id=sid, animal_id=animal_id, photo_id=second)
    assert [p["is_main"] for p in _photos(app, animal_id)] == [0, 1]


def test_removing_main_photo_promotes_next(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    first = _photo(app, actor, sid, animal_id, "1.jpg")
    _photo(app, actor, sid, animal_id, "2.jpg")

    path = _run(app, RemoveAnimalPhotoCommand, shelter_id=sid, animal_id=animal_id, photo_id=first)
    assert path == "uploads/animals/1.jpg"  # route usunie plik
    remaining = _photos(app, animal_id)
    assert [(p["file_path"], p["is_main"]) for p in remaining] == [("uploads/animals/2.jpg", 1)]


def test_photo_operations_are_scoped_to_shelter(app, world):
    animal_a = _animal(app, world["manager_a"], world["shelter_a"])
    photo = _photo(app, world["manager_a"], world["shelter_a"], animal_a)
    # Placówka B zna ID zdjęcia i karty A, ale nie ma do nich dostępu.
    for cls, kwargs in (
        (RemoveAnimalPhotoCommand, {"photo_id": photo}),
        (SetMainAnimalPhotoCommand, {"photo_id": photo}),
    ):
        with pytest.raises(NotFoundError):
            _run(app, cls, shelter_id=world["shelter_b"], animal_id=animal_a, **kwargs)
    with pytest.raises(NotFoundError):
        _run(app, AddAnimalPhotoCommand, actor_id=world["manager_b"], shelter_id=world["shelter_b"],
             animal_id=animal_a, file_path="uploads/animals/x.jpg")
    assert len(_photos(app, animal_a)) == 1


def test_photo_from_other_animal_is_not_found(app, world):
    actor, sid = world["manager_a"], world["shelter_a"]
    one, two = _animal(app, actor, sid, "Jeden"), _animal(app, actor, sid, "Dwa")
    photo_of_two = _photo(app, actor, sid, two)
    with pytest.raises(NotFoundError):
        _run(app, SetMainAnimalPhotoCommand, shelter_id=sid, animal_id=one, photo_id=photo_of_two)


# --- Publikacja, wycofanie, aktualność ----------------------------------

def _publish(app, actor, sid, animal_id):
    _run(app, PublishAnimalProfileCommand, actor_id=actor, shelter_id=sid, animal_id=animal_id)


def _published(app, world, name="Burek", **profile):
    animal_id = _animal(app, world["manager_a"], world["shelter_a"], name, **profile)
    _photo(app, world["manager_a"], world["shelter_a"], animal_id, f"{name}.jpg")
    _publish(app, world["manager_a"], world["shelter_a"], animal_id)
    return animal_id


def test_unapproved_shelter_has_draft_but_cannot_publish(app, world):  # AC-004
    actor, sid = world["manager_c"], world["shelter_c"]
    animal_id = _animal(app, actor, sid)
    _photo(app, actor, sid, animal_id)
    with pytest.raises(BusinessRuleError, match="zatwierdzeniu placówki"):
        _publish(app, actor, sid, animal_id)
    assert _row(app, animal_id)["status"] == "Draft"


def test_publish_requires_complete_profile_and_photo(app, world):  # BR-008
    actor, sid = world["manager_a"], world["shelter_a"]
    animal_id = _animal(app, actor, sid)
    with pytest.raises(BusinessRuleError, match="co najmniej jedno zdjęcie"):
        _publish(app, actor, sid, animal_id)

    empty = _run(app, CreateAnimalProfileCommand, actor_id=actor, shelter_id=sid,
                 name="Pusty", species="Cat")
    _photo(app, actor, sid, empty)
    with pytest.raises(BusinessRuleError, match="opis charakteru.*wielkość"):
        _publish(app, actor, sid, empty)


def test_publish_sets_dates_and_cannot_repeat(app, world):
    animal_id = _published(app, world)
    row = _row(app, animal_id)
    assert row["status"] == "Available"
    assert row["published_at"] and row["last_confirmed_at"]
    assert row["last_confirmed_by"] == world["manager_a"]
    with pytest.raises(BusinessRuleError, match="obecnym statusie"):
        _publish(app, world["manager_a"], world["shelter_a"], animal_id)


def test_cannot_remove_last_photo_of_published_card(app, world):  # BR-008
    animal_id = _published(app, world)
    (photo,) = _photos(app, animal_id)
    with pytest.raises(BusinessRuleError, match="co najmniej jedno zdjęcie"):
        _run(app, RemoveAnimalPhotoCommand, shelter_id=world["shelter_a"],
             animal_id=animal_id, photo_id=photo["id"])
    # Po dodaniu drugiego zdjęcia usunięcie pierwszego jest już dozwolone.
    _photo(app, world["manager_a"], world["shelter_a"], animal_id, "drugie.jpg")
    _run(app, RemoveAnimalPhotoCommand, shelter_id=world["shelter_a"],
         animal_id=animal_id, photo_id=photo["id"])
    assert len(_photos(app, animal_id)) == 1


def test_withdraw_requires_reason_and_disables_donations(app, world):
    animal_id = _published(app, world)
    _sql(app, "UPDATE animals SET donations_enabled = 1 WHERE id = :id", id=animal_id)
    args = dict(actor_id=world["manager_a"], shelter_id=world["shelter_a"], animal_id=animal_id)
    with pytest.raises(BusinessRuleError, match="powód"):
        _run(app, WithdrawAnimalProfileCommand, reason="  ", **args)

    _run(app, WithdrawAnimalProfileCommand, reason="Pies wrócił do właściciela.", **args)
    row = _row(app, animal_id)
    assert (row["status"], row["donations_enabled"]) == ("Withdrawn", 0)
    assert row["withdrawn_reason"] == "Pies wrócił do właściciela."
    with pytest.raises(BusinessRuleError, match="tylko opublikowaną"):
        _run(app, WithdrawAnimalProfileCommand, reason="Jeszcze raz", **args)


def test_withdrawn_card_can_be_republished(app, world):
    animal_id = _published(app, world)
    args = dict(actor_id=world["manager_a"], shelter_id=world["shelter_a"], animal_id=animal_id)
    _run(app, WithdrawAnimalProfileCommand, reason="Pomyłka", **args)
    _publish(app, world["manager_a"], world["shelter_a"], animal_id)
    row = _row(app, animal_id)
    assert (row["status"], row["withdrawn_reason"]) == ("Available", None)


def test_confirm_saves_person_and_can_correct_age(app, world):  # AC-017, D8
    animal_id = _published(app, world)
    _sql(app, """UPDATE animals SET last_confirmed_at = '2026-01-01T00:00:00Z',
                 last_confirmed_by = :admin WHERE id = :id""", id=animal_id, admin=world["admin"])
    args = dict(actor_id=world["manager_a"], shelter_id=world["shelter_a"], animal_id=animal_id)

    _run(app, ConfirmAnimalProfileAccuracyCommand, **args)  # bez korekty wieku
    row = _row(app, animal_id)
    assert row["last_confirmed_at"] > "2026-01-01T00:00:00Z"
    assert row["last_confirmed_by"] == world["manager_a"]
    assert (row["age_min_months"], row["age_max_months"]) == (24, 36)

    _run(app, ConfirmAnimalProfileAccuracyCommand, age_min_months=30, age_max_months=42, **args)
    row = _row(app, animal_id)
    assert (row["age_min_months"], row["age_max_months"]) == (30, 42)


def test_confirm_only_for_published_cards(app, world):
    animal_id = _animal(app, world["manager_a"], world["shelter_a"])
    with pytest.raises(BusinessRuleError, match="opublikowanej"):
        _run(app, ConfirmAnimalProfileAccuracyCommand, actor_id=world["manager_a"],
             shelter_id=world["shelter_a"], animal_id=animal_id)