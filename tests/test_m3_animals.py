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
from operations.animal.GetAnimalProfileQuery import GetAnimalProfileQuery
from operations.animal.HideAnimalProfileCommand import HideAnimalProfileCommand
from operations.animal.ListAnimalsForModerationQuery import ListAnimalsForModerationQuery
from operations.animal.SearchAnimalsQuery import SearchAnimalsQuery
from operations.animal.UnhideAnimalProfileCommand import UnhideAnimalProfileCommand
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


# --- Katalog (SearchAnimalsQuery, GetAnimalProfileQuery) ------------------

def _search(app, **filters):
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        return SearchAnimalsQuery(conn).execute(**filters)


def _names(result):
    return [a["name"] for a in result["items"]]


def _catalog(app, world):
    """Cztery opublikowane karty w dwóch placówkach + jeden szkic."""
    burek = _published(app, world, "Burek", size="Medium", age_min_months=24, age_max_months=36)
    maly = _published(app, world, "Maly", size="Small", age_min_months=6, age_max_months=12)
    mruczek = _published(app, world, "Mruczek", species="Cat", size="Small",
                         age_min_months=48, age_max_months=60, sex="Female")
    # Placówka B (kujawsko-pomorskie).
    reks = _animal(app, world["manager_b"], world["shelter_b"], "Reks", size="Medium",
                   age_min_months=30, age_max_months=40)
    _photo(app, world["manager_b"], world["shelter_b"], reks, "reks.jpg")
    _publish(app, world["manager_b"], world["shelter_b"], reks)
    _animal(app, world["manager_a"], world["shelter_a"], "Szkic")
    return {"burek": burek, "maly": maly, "mruczek": mruczek, "reks": reks}


def test_catalog_shows_only_available_cards_by_default(app, world):  # BR-012, BR-020
    _catalog(app, world)
    assert sorted(_names(_search(app))) == ["Burek", "Maly", "Mruczek", "Reks"]


def test_filters_work_together(app, world):  # AC-001, BR-016
    ids = _catalog(app, world)
    # Psy, kujawsko-pomorskie, średnie, wiek 2-6 lat (24-72 mies.).
    result = _search(app, species="Dog", voivodeship="kujawsko-pomorskie", sizes="Medium",
                     age_from_months=24, age_to_months=72)
    assert _names(result) == ["Reks"]
    # Ten sam zestaw bez województwa: dochodzi Burek z placówki A.
    assert sorted(_names(_search(app, species="Dog", sizes="Medium",
                                 age_from_months=24, age_to_months=72))) == ["Burek", "Reks"]
    assert _names(_search(app, sex="Female")) == ["Mruczek"]
    assert sorted(_names(_search(app, sizes="Small,Medium", species="Dog"))) == ["Burek", "Maly", "Reks"]
    assert _names(_search(app, shelter_id=world["shelter_b"])) == ["Reks"]  # BR-017
    assert _names(_search(app, text="mrucz")) == ["Mruczek"]
    assert _names(_search(app, city="Bydgosz")) == ["Reks"]
    assert ids  # fixture zwrócił ID


def test_age_filter_uses_range_overlap(app, world):  # BR-016
    _catalog(app, world)
    # Burek ma 24-36 mies.: zahacza o przedział 36-48 tylko górną granicą.
    assert "Burek" in _names(_search(app, species="Dog", age_from_months=36, age_to_months=48))
    assert "Burek" not in _names(_search(app, species="Dog", age_from_months=37, age_to_months=48))
    # Sama dolna granica (bez górnej) i sama górna.
    assert "Maly" not in _names(_search(app, species="Dog", age_from_months=24))
    assert _names(_search(app, species="Dog", age_to_months=12)) == ["Maly"]


def test_cards_without_age_do_not_match_age_filter(app, world):
    animal_id = _animal(app, world["manager_a"], world["shelter_a"], "Bezwiekowy",
                        age_min_months=-1, age_max_months=-1)
    # Bez wieku nie da się opublikować, więc wymuszamy stan w bazie wprost.
    _photo(app, world["manager_a"], world["shelter_a"], animal_id)
    _sql(app, """UPDATE animals SET status='Available', published_at='2026-01-01T00:00:00Z',
                 last_confirmed_at='2026-01-01T00:00:00Z' WHERE id=:id""", id=animal_id)
    assert "Bezwiekowy" in _names(_search(app))
    assert "Bezwiekowy" not in _names(_search(app, age_from_months=0, age_to_months=1000))


def test_hidden_withdrawn_and_unapproved_cards_are_not_listed(app, world):  # BR-012, R6
    ids = _catalog(app, world)
    _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["burek"], reason="Skarga")
    _run(app, WithdrawAnimalProfileCommand, actor_id=world["manager_a"],
         shelter_id=world["shelter_a"], animal_id=ids["maly"], reason="Adopcja poza portalem")
    assert sorted(_names(_search(app))) == ["Mruczek", "Reks"]
    # Zablokowana placówka znika z katalogu razem z kartami (D13), bez zmiany ich statusu.
    _run(app, BlockShelterCommand, actor_id=world["admin"], shelter_id=world["shelter_b"], reason="X")
    assert _names(_search(app)) == ["Mruczek"]
    assert _row(app, ids["reks"])["status"] == "Available"


def test_unhide_restores_card(app, world):
    ids = _catalog(app, world)
    _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["burek"], reason="Skarga")
    with pytest.raises(BusinessRuleError, match="już ukryta"):
        _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["burek"], reason="Jeszcze raz")
    _run(app, UnhideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["burek"])
    assert "Burek" in _names(_search(app))
    with pytest.raises(BusinessRuleError, match="nie jest ukryta"):
        _run(app, UnhideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["burek"])


def test_hide_requires_reason_and_leaves_status(app, world):
    animal_id = _published(app, world)
    with pytest.raises(BusinessRuleError, match="powód"):
        _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=animal_id, reason=" ")
    _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=animal_id, reason="Skarga")
    row = _row(app, animal_id)
    assert (row["status"], row["is_hidden"], row["hidden_by"]) == ("Available", 1, world["admin"])
    with pytest.raises(NotFoundError):
        _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=9999, reason="x")


def test_in_progress_cards_only_with_flag(app, world):  # BR-020
    ids = _catalog(app, world)
    _sql(app, "UPDATE animals SET status = 'AdoptionInProgress' WHERE id = :id", id=ids["burek"])
    assert "Burek" not in _names(_search(app))
    assert "Burek" in _names(_search(app, include_in_progress=True))


def test_sorting_by_publication_and_confirmation(app, world):  # BR-019
    ids = _catalog(app, world)
    _sql(app, "UPDATE animals SET published_at = '2026-03-01T00:00:00Z', last_confirmed_at = '2026-05-01T00:00:00Z' WHERE id = :id", id=ids["burek"])
    _sql(app, "UPDATE animals SET published_at = '2026-04-01T00:00:00Z', last_confirmed_at = '2026-02-01T00:00:00Z' WHERE id = :id", id=ids["maly"])
    _sql(app, "UPDATE animals SET published_at = '2026-01-01T00:00:00Z', last_confirmed_at = '2026-01-01T00:00:00Z' WHERE id IN (:a, :b)", a=ids["mruczek"], b=ids["reks"])
    by_published = _names(_search(app, sort="published"))
    by_confirmed = _names(_search(app, sort="confirmed"))
    assert by_published[:2] == ["Maly", "Burek"]
    assert by_confirmed[:2] == ["Burek", "Maly"]


def test_needs_confirmation_after_30_days_and_confirm_clears_it(app, world):  # AC-016, AC-017
    animal_id = _published(app, world)
    assert _search(app)["items"][0]["needs_confirmation"] == 0
    _sql(app, "UPDATE animals SET last_confirmed_at = strftime('%Y-%m-%dT%H:%M:%SZ','now','-31 days') WHERE id = :id", id=animal_id)
    assert _search(app)["items"][0]["needs_confirmation"] == 1
    # Karta zostaje w katalogu (BR-045), tylko z ostrzeżeniem.
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        assert GetAnimalProfileQuery(conn).execute(animal_id)["needs_confirmation"] == 1

    _run(app, ConfirmAnimalProfileAccuracyCommand, actor_id=world["manager_a"],
         shelter_id=world["shelter_a"], animal_id=animal_id)
    assert _search(app)["items"][0]["needs_confirmation"] == 0


def test_public_profile_has_details_and_no_hidden_cards(app, world):  # AC-003
    animal_id = _published(app, world)
    _run(app, UpdateAnimalCareRequirementsCommand, actor_id=world["manager_a"],
         shelter_id=world["shelter_a"], animal_id=animal_id, good_with_children="Yes",
         good_with_dogs="Unknown", good_with_cats="No", special_care_required="No")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        animal = GetAnimalProfileQuery(conn).execute(animal_id)
        assert animal["shelter_name"] == "Schronisko A"
        assert animal["temperament_tags"] == ["łagodny", "towarzyski"]
        assert animal["requirements"]["good_with_dogs"] == "Unknown"
        assert len(animal["photos"]) == 1 and animal["photos"][0]["is_main"] == 1
        assert "contact_name" not in animal and "submitted_by" not in animal
    _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=animal_id, reason="x")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        assert GetAnimalProfileQuery(conn).execute(animal_id) is None
        assert GetAnimalProfileQuery(conn).execute(9999) is None


def test_moderation_list_shows_all_shelters_and_hidden_first(app, world):
    ids = _catalog(app, world)
    _run(app, HideAnimalProfileCommand, actor_id=world["admin"], animal_id=ids["reks"], reason="x")
    with app.app_context(), app.extensions["db_engine"].connect() as conn:
        query = ListAnimalsForModerationQuery(conn)
        result = query.execute()
        assert result["items"][0]["name"] == "Reks"
        assert result["pagination"]["total"] == 5  # z szkicem
        assert [a["name"] for a in query.execute(hidden_only=True)["items"]] == ["Reks"]
        assert [a["name"] for a in query.execute(search="Schronisko B")["items"]] == ["Reks"]


# --- Trasy panelu (szkic, edycja, wymagania) ------------------------------

def _panel(sid, suffix=""):
    return f"/panel/shelters/{sid}/animals{suffix}"


def test_panel_draft_flow(app, client, world):
    sid = world["shelter_a"]
    _login(client, "a@example.com")

    assert client.get(_panel(sid)).status_code == 200
    assert client.get(_panel(sid, "/new")).status_code == 200
    resp = client.post(_panel(sid), data={"name": "Bonifacy", "species": "Dog"})
    assert resp.status_code == 303
    animal_id = _sql(app, "SELECT id FROM animals WHERE name = 'Bonifacy'")[0]["id"]
    assert resp.headers["Location"].endswith(_panel(sid, f"/{animal_id}/edit"))
    assert client.get(_panel(sid, f"/{animal_id}/edit")).status_code == 200

    resp = client.post(_panel(sid, f"/{animal_id}"), data={
        "name": "Bonifacy", "species": "Dog", "sex": "Male", "breed": "Owczarek",
        "size": "Large", "age_min_months": "18", "age_max_months": "",
        "description": "Radosny.", "daily_needs": "Długie spacery.", "temperament": "żywy",
    })
    assert resp.status_code == 303
    row = _row(app, animal_id)
    assert (row["breed"], row["size"], row["age_min_months"], row["age_max_months"]) == ("Owczarek", "Large", 18, 18)

    resp = client.post(_panel(sid, f"/{animal_id}/requirements"), data={
        "good_with_children": "Yes", "good_with_dogs": "No", "good_with_cats": "Unknown",
        "special_care_required": "No", "activity_level": "High", "min_experience": "",
    })
    assert resp.status_code == 303

    page = client.get(_panel(sid, f"/{animal_id}")).get_data(as_text=True)
    assert "Bonifacy" in page and "1 rok 6 mies." in page and "Owczarek" in page
    assert "Przed publikacją uzupełnij: co najmniej jedno zdjęcie" in page
    assert "Bonifacy" in client.get(_panel(sid)).get_data(as_text=True)


def test_panel_business_error_flashes_and_returns(app, client, world):
    _login(client, "a@example.com")
    resp = client.post(_panel(world["shelter_a"]), data={"name": " ", "species": "Dog"},
                       headers={"Referer": "http://localhost" + _panel(world["shelter_a"], "/new")})
    assert resp.status_code == 303 and resp.headers["Location"].endswith("/animals/new")
    assert "Imię: pole nie może być puste" in client.get(_panel(world["shelter_a"], "/new")).get_data(as_text=True)
    assert _sql(app, "SELECT COUNT(*) AS n FROM animals")[0]["n"] == 0


def test_panel_is_isolated_between_shelters(app, client, world):  # AC-005
    animal_b = _animal(app, world["manager_b"], world["shelter_b"], "Cudzy")
    _login(client, "a@example.com")
    # Cudza placówka: 403 dla każdej akcji.
    assert client.get(_panel(world["shelter_b"])).status_code == 403
    assert client.post(_panel(world["shelter_b"]), data={"name": "X", "species": "Dog"}).status_code == 403
    # Własna placówka, ale ID cudzej karty: 404 (wspólna przestrzeń ID nie przecieka).
    for suffix in ("", "/edit", "/requirements"):
        assert client.get(_panel(world["shelter_a"], f"/{animal_b}{suffix}")).status_code == 404
    resp = client.post(_panel(world["shelter_a"], f"/{animal_b}"), data={
        "name": "Hak", "species": "Dog", "sex": "Male", "description": "", "daily_needs": ""})
    assert resp.status_code == 404
    assert _row(app, animal_b)["name"] == "Cudzy"


def test_panel_requires_login_and_blocks_read_only_shelter(app, client, world):
    assert client.get(_panel(world["shelter_a"])).status_code == 302  # → /login
    _run(app, BlockShelterCommand, actor_id=world["admin"], shelter_id=world["shelter_a"], reason="X")
    _login(client, "a@example.com")
    assert client.get(_panel(world["shelter_a"])).status_code == 200  # odczyt działa (R5)
    assert client.post(_panel(world["shelter_a"]), data={"name": "X", "species": "Dog"}).status_code == 403


def test_pending_shelter_can_prepare_drafts_in_panel(app, client, world):  # R3, AC-004
    _login(client, "c@example.com")
    resp = client.post(_panel(world["shelter_c"]), data={"name": "Szkicowy", "species": "Cat"})
    assert resp.status_code == 303
    assert _sql(app, "SELECT status FROM animals WHERE name = 'Szkicowy'")[0]["status"] == "Draft"


def test_dashboard_shows_animal_counters(app, client, world):
    _published(app, world)
    _sql(app, "UPDATE animals SET last_confirmed_at = strftime('%Y-%m-%dT%H:%M:%SZ','now','-40 days')")
    _login(client, "a@example.com")
    page = client.get(f"/panel/shelters/{world['shelter_a']}").get_data(as_text=True)
    assert "do potwierdzenia: 1" in page and "do adopcji: 1" in page


def test_format_age_in_polish():
    from labels import format_age

    assert format_age(None, None) == "wiek nieustalony"
    assert format_age(8, 8) == "8 mies."
    assert format_age(12, 12) == "1 rok"
    assert format_age(24, 24) == "2 lata"
    assert format_age(60, 60) == "5 lat"
    assert format_age(144, 144) == "12 lat"  # nie „12 lata”
    assert format_age(18, 30) == "1 rok 6 mies. – 2 lata 6 mies."