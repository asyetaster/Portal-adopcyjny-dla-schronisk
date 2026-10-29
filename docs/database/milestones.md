# Plan implementacji: milestone'y

Każdy milestone to **kompletna ścieżka** (operacje + routes + szablony + dane demo), którą da się pokazać w przeglądarce i zmergować jako jeden PR (albo kilka mniejszych). Zależności:

```text
     ┌→ M0.5 (layout) ─┐
M0 ──┤                 ├→ M2 → M3 ─┬→ M4 → M5 ─┐
     └→ M1 ────────────┘           ├→ M6 ──────┼→ M9 → M10
                                   ├→ M7 ──────┤
                                   └→ M8 ──────┘
```

M0.5 (wygląd) i M1 (konta) można robić równolegle, np. jedna osoba robi frontend, druga backend. Oba muszą być gotowe przed M2, bo od M2 powstają szablony, które dziedziczą z layoutów. Po M3 moduły M4+M5, M6, M7 i M8 są od siebie niezależne i mogą powstawać równolegle (np. każda osoba w zespole bierze jeden). M7 korzysta z M6 tylko przy wymogu „zaakceptowany wolontariusz”; do czasu M6 ten warunek może zwracać `False`.

| # | Milestone | Ścieżka z §12 | Operacje | Kryteria akceptacji |
|---|---|---|---|---|
| M0 | Fundamenty | — | 0 | — |
| M0.5 | Layout i komponenty | — | 0 | podstawa pod AC-020 |
| M1 | Konta i logowanie | 1 | 11 | BR-050 |
| M2 | Schroniska | 1 | 16 | AC-005, BR-014 |
| M3 | Karty zwierząt i katalog | 2 | 18 | AC-001…004, 016, 017 |
| M4 | Ulubione, profil warunków, dopasowanie | 3 | 6 | AC-006…009 |
| M5 | Zgłoszenia adopcyjne | 4 | 11 | AC-010…015, 018, 019 |
| M6 | Wolontariat | 5 | 13 | AC-029…032 |
| M7 | Spacery | 6 | 18 | AC-033…041 |
| M8 | Wsparcie finansowe | 7 | 18 | AC-021…028, 042 |
| M9 | Prywatność, moderacja, zadania systemowe | 8 | 6 | AC-019, BR-046, BR-048, BR-051 |
| M10 | Dane demo i odbiór | 8 | 1 | AC-020 + przegląd wszystkich AC |

---

## Zasady wspólne

Obowiązują w każdym milestonie. Ustala je M0.

### Operacje (`operations/`)

1. **Jedna klasa w jednym pliku:** `operations/<moduł>/<Nazwa>Command.py` / `...Query.py`, nazwa klasy unikalna w całym pakiecie (wymaga tego `cli.discover_operations`). Nazwa = nazwa use case'u + sufiks, np. `RegisterUser` → `RegisterUserCommand`.
2. **`execute()` przyjmuje tylko `str`, `int`, `float`, `bool`.** To wymóg runnera `test.py`, który przy jednym nieobsługiwanym typie (np. `str | None`, `list`) przestaje działać dla **wszystkich** operacji. Dlatego:
   - pole opcjonalne tekstowe: `str = ""`, a command zapisuje `NULL`, gdy dostanie `""`,
   - opcjonalny `int` (wiek, kwota maksymalna, ID): `-1` = brak dla wartości, które mogą być zerem; `0` = brak dla ID,
   - wartość trójstanowa (tak / nie / brak odpowiedzi): `str` z wartościami `"1"`, `"0"`, `""`,
   - lista: `str` rozdzielony przecinkami, a command zapisuje JSON,
   - data i czas: `str` w ISO-8601 UTC.
3. **Kto działa:** commandy wykonywane w imieniu użytkownika przyjmują `actor_id: int` (do kolumn `*_by`) albo `user_id: int` (dla operacji „moje”). Uprawnienie do zasobu sprawdza route (patrz niżej), a reguły biznesowe command.
4. **Zakres placówki:** operacje panelu przyjmują `shelter_id: int` i zawsze filtrują `WHERE id = :id AND shelter_id = :shelter_id`. Podmiana ID w adresie nie może dać dostępu do danych innej placówki (BR-049, AC-005).
5. **Błędy:** `operations/errors.py` z klasami `NotFoundError` i `BusinessRuleError(message)`, gdzie komunikat jest gotowy do pokazania użytkownikowi. Wyjątek w commandzie = rollback całej transakcji (robi to `@page`).
6. **Zwracane wartości:** Command zwraca ID nowego wiersza albo `None`. Query zwraca `dict` / `None` albo słownik stronicowania w formacie `ListUsersQuery` (`items` + `pagination`), budowany przez wspólny helper `operations/pagination.py` (logika przeniesiona z obecnego `ListUsersQuery`).
7. **Wspólny kod w `operations/common.py`:**
   - `now_utc()`: aktualny czas jako ISO-8601 UTC,
   - fragmenty SQL z warunkami widoczności i zapisu, np. `VISIBLE_ANIMAL_SQL`,
   - `record_event(connection, table, application_id, type, from_status, to_status, message, author_id)`, czyli wpis do `*_application_events`,
   - `end_animal_activity(connection, animal_id, reason)` (R7), rozbudowywana w M3, M5 i M7.
8. **Każdy command z efektem w kilku tabelach** robi wszystko w transakcji otwartej przez `@page` / runner. Żadnych własnych `commit()`.
9. **Test z konsoli:** każdą operację da się wywołać przez `python test.py <Klasa> --param ...`, także zadania systemowe i administracyjne (`MakeAdminCommand`, `SeedDemoDataCommand`). Dzięki temu nie trzeba dopisywać osobnych komend do `cli.py`.

### Routes (`routes/`)

1. **Jeden plik na endpoint** z funkcją `register(app)`, jak w `routes/user/`. Układ katalogów `routes/<obszar>/<moduł>/<akcja>.py`.
2. **Cztery obszary:**

   | Obszar | Prefiks URL | Kto | Layout |
   |---|---|---|---|
   | `public` | `/` | każdy | `public/base.html` |
   | `account` | `/account/...` | zalogowany | `public/base.html` |
   | `panel` | `/panel/shelters/<int:shelter_id>/...` | pracownik tej placówki | `panel/base.html` |
   | `admin` | `/admin/...` | `is_admin = 1` | `admin/base.html` |

3. **Nazwy funkcji widoków = nazwy endpointów Flaska, muszą być unikalne:** `<obszar>_<moduł>_<akcja>`, np. `panel_animals_publish`. Tabele poniżej podają ścieżkę pliku, a nazwa funkcji wynika z niej.
4. **Dostęp:** `auth.py` w katalogu głównym definiuje dekoratory `login_required`, `admin_required`, `shelter_required(manager=False)`. Czytają `g.user` ustawiane w `before_request` (M1). Dekorator stoi **między** `@app.get/post` a `@page`, więc odmowa następuje przed otwarciem transakcji:

   ```python
   @app.post("/panel/shelters/<int:shelter_id>/animals/<int:animal_id>/publish")
   @shelter_required()
   @page("panel/animals/details.html", write=True)
   def panel_animals_publish(shelter_id: int, animal_id: int, publish: PublishAnimalProfileCommand):
       publish.execute(actor_id=g.user["id"], shelter_id=shelter_id, animal_id=animal_id)
       flash("Karta opublikowana.")
       return redirect(url_for("panel_animals_details", shelter_id=shelter_id, animal_id=animal_id), code=303)
   ```

5. **POST zawsze kończy się przekierowaniem** (Post/Redirect/Get, kod 303) z `flash()`, jak w `routes/user/create.py`.
6. **Walidacja formularzy** w helperach `routes/<obszar>/<moduł>/__init__.py` (wzór: `read_user_name`), a przy złych danych `abort(400)`.
7. **Obsługa błędów:** `routes/errors.py` (`register(app)` z `app.register_error_handler`): `BusinessRuleError` → `flash(komunikat)` + przekierowanie na `request.referrer`; `NotFoundError` → 404. Widoki nie łapią tych wyjątków same.
8. **E-maile:** `mailer.py` z funkcją `queue_mail(to, subject, template, **ctx)`. W kontekście requestu zapisuje maila w `g`, a `after_request` (w `routes/mail.py`) wysyła go tylko przy odpowiedzi < 400, czyli po commicie. Poza requestem (`test.py`) wysyła od razu. W trybie deweloperskim zamiast SMTP dopisuje do `instance/mails.log`.

### Szablony (`templates/`)

1. **Layouty** (powstają w [M0.5](#m05-layout-i-komponenty)):
   - `public/base.html` + `account/base.html`: strona klienta, czysty CSS z makiet `docs/*.html`; zastępuje obecny `templates/base.html`,
   - `backoffice/base.html`: wspólny szkielet panelu i administracji na Bootstrapie, z kolorami portalu,
   - `panel/base.html`: sidebar z modułami placówki (karty, zgłoszenia, wolontariat, spacery, wpłaty, personel) i przełącznik placówki,
   - `admin/base.html`: istniejący, przepięty na `backoffice/base.html`, z prawdziwym menu.
2. **Komponenty:** makra w `templates/components/` (lista w M0.5). Nowe strony składa się z nich, bez własnego HTML-a dla kart, plakietek, pól formularza i paginacji, i **bez własnych bloków `<style>`**. Kiedy komponentu brakuje, dopisuje się go do `components/` i do `/styleguide`.
3. **Polskie etykiety enumów w jednym miejscu:** `labels.py` ze słownikiem `{"adoption": {"InContact": "W kontakcie", ...}, ...}`, zarejestrowany jako filtr Jinja `|label` (`{{ app.status|label("adoption") }}`) w `routes/filters.py`.
4. **Makiety → szablony:**

   | Makieta | Szablon | Milestone |
   |---|---|---|
   | `docs/widok_glowny.html` | `public/home.html` | M3 |
   | `docs/portal-katalog-schronisk.html` | `public/shelters/list.html` | M2 |
   | `docs/portal-profil-schroniska.html` | `public/shelters/details.html` | M2, uzupełniany w M3, M6–M8 |
   | `docs/karta_zwierzaka.html` | `public/animals/details.html` | M3, uzupełniany w M4, M7, M8 |
   | `docs/portal-wolontariat.html` | `public/volunteering/offer.html` | M6 |
   | `docs/portal-spacery.html` | `public/walks/list.html` | M7 |
   | `docs/portal-wsparcie.html` | `public/donations/start.html` | M8 |

### Dane demo

`operations/demo/SeedDemoDataCommand.py` powstaje w M1, a **każdy milestone go rozszerza** o dane swojego modułu. Uruchamianie: `python test.py SeedDemoDataCommand`. Wszystkie konta demo mają hasło `demo1234`. Dzięki temu każdy PR da się obejrzeć bez ręcznego klikania.

---

## M0. Fundamenty

**Cel:** nowy schemat i infrastruktura wspólna, bez funkcji biznesowych.

**Zadania:**

| Plik | Zmiana |
|---|---|
| `schema.sql` | Zastąpić zawartością `docs/db-diagram/schema.sql`. |
| `database.py` | W `_on_connect`: `PRAGMA foreign_keys = ON`. W `_on_begin`: `BEGIN IMMEDIATE`, gdy `connection.info.get("begin_immediate")`, a w przeciwnym razie `BEGIN` (D11). |
| `web.py` | Przed `connection.begin()`: `connection.info["begin_immediate"] = write`. |
| `cli.py` | W `run_operation` to samo dla commandów: `connection.info["begin_immediate"] = is_command(cls)`. |
| `operations/user/*`, `routes/user/*`, `templates/admin/users/*` | Usunąć. Wracają w M1 jako `operations/identity/*` i `routes/admin/users/*` pod nową tabelę `users`. |
| `operations/errors.py`, `operations/pagination.py`, `operations/common.py` | Nowe (zasady wspólne pkt 5–7). `common.py` na razie tylko z `now_utc()`. |
| `auth.py` | Szkielet dekoratorów (bez `before_request`, który powstaje w M1). |
| `labels.py`, `routes/filters.py` | Filtr `|label`. |
| `mailer.py`, `routes/mail.py` | Kolejka e-maili + zapis do `instance/mails.log`. |
| `routes/errors.py` | Obsługa `BusinessRuleError` i `NotFoundError`, strony 403 / 404. |
| `templates/public/base.html`, `templates/panel/base.html`, `templates/errors/{403,404}.html` | Najprostsze wersje (sam szkielet HTML z `{% block content %}`), żeby M1 miał z czego dziedziczyć. Docelowy wygląd powstaje w M0.5. |
| `routes/public/home/show.py` + `templates/public/home.html` | `GET /`: pusta strona główna. |

**Gotowe, gdy:** `flask --app app run` startuje na nowym schemacie, `/` renderuje stronę główną, `python test.py --help` działa (lista operacji może być pusta), naruszenie klucza obcego w SQLite kończy się błędem.

---

## M0.5. Layout i komponenty

**Cel:** spójny wygląd strony klienta zbudowany z makiet `docs/*.html` oraz zestaw komponentów, z których korzystają szablony wszystkich kolejnych milestone'ów. Bez logiki i bez nowych operacji.
**Zależy od:** M0. **Równolegle z:** M1. **Musi być gotowe przed:** M2.

**Dlaczego teraz:** od M2 każdy milestone dodaje kilka do kilkunastu szablonów. Jeśli layout i komponenty istnieją wcześniej, każda nowa strona wygląda dobrze od razu. Robienie wyglądu na końcu oznacza przerabianie ~80 szablonów.

### Strona klienta (obowiązkowo)

Makiety nie używają frameworka CSS: każda ma własny `<style>` z tymi samymi zmiennymi (`--bg`, `--surface`, `--ink`, `--muted`, `--line`, `--brand`, `--sun`...). Zostajemy przy czystym CSS, bez Bootstrapa na stronie klienta.

| Plik | Zawartość |
|---|---|
| `static/css/tokens.css` | Zmienne z makiet (kolory, typografia, odstępy, promienie, cienie) w jednym miejscu. Wspólne dla strony klienta i panelu. |
| `static/css/public.css` | Reset, typografia, siatka, nagłówek i stopka, przyciski, formularze, karty, tabele, plakietki, alerty (flash), paginacja. Klasy wyciągnięte z makiet i ujednolicone, bez kopiowania `<style>` do każdej strony. Mobile-first (punkty przełamania 640 / 1024 px). |
| `static/img/` | Logo, favicon, zdjęcie zastępcze dla karty bez zdjęcia. |
| `templates/public/base.html` | Nagłówek z nawigacją (Zwierzęta, Schroniska, Spacery, Wsparcie), menu konta (zaloguj / moje konto / panel placówki / admin, zależnie od `g.user`), flash, stopka; menu mobilne bez JS (`<details>`). |
| `templates/account/base.html` | Rozszerza `public/base.html`: boczne menu „Moje konto” (profil, profil warunków, ulubione, zgłoszenia, wolontariat, spacery, wpłaty, moje placówki). |

**Komponenty** (makra Jinja w `templates/components/`, każde z krótkim komentarzem „jak użyć”, jak w `_pagination.html`):

| Makro | Używane w |
|---|---|
| `animal_card(animal)` | katalog, strona główna, profil schroniska, ulubione (M3, M4) |
| `status_badge(value, kind)` | wszystkie listy zgłoszeń, kart, terminów, wpłat (korzysta z filtra `|label`) |
| `field(name, label, value, type, required, help, error)`, `select(...)`, `tristate(...)`, `checkbox(...)` | wszystkie formularze; `tristate` = tak / nie / bez odpowiedzi (M4) |
| `filters_bar(...)` | katalog zwierząt, schronisk, spacerów (M2, M3, M7) |
| `empty_state(text, action_url, action_label)` | puste listy |
| `timeline(events)` | historia zgłoszeń (M5, M6) |
| `compatibility(items)` | dopasowanie (M4, M5) |
| `notice(kind, text)` | informacje typu „zgłoszenie to nie rezerwacja” (BR-035), „dostępność wymaga potwierdzenia” (BR-045) |
| `pagination(...)` | istniejący `_pagination.html` przeniesiony do `components/` i ostylowany dla strony klienta |

**Strona wzorcowa:** `GET /styleguide` (`routes/public/styleguide/show.py` + `templates/public/styleguide.html`), dostępna tylko przy `app.debug`. Pokazuje wszystkie komponenty z przykładowymi danymi. Osoby robiące M2–M8 sprawdzają tam, czego użyć, zamiast pisać własny HTML.

### Panel placówki i administracja (opcjonalnie, tanio teraz)

Panel i admin zostają na Bootstrapie (już jest w `admin/base.html`, a tabele i formularze back-office wychodzą w nim najszybciej). W M0.5 tylko:

| Plik | Zmiana |
|---|---|
| `templates/backoffice/base.html` | Wspólny szkielet obecnego `admin/base.html` (sidebar + main + flash). `admin/base.html` i `panel/base.html` tylko go rozszerzają i podają własne menu, więc wygląd poprawia się w jednym miejscu. |
| `static/css/backoffice.css` | Kolory Bootstrapa nadpisane zmiennymi z `tokens.css` (`--bs-primary` = `--brand` itd.), ten sam font co na stronie klienta. Panel wygląda jak część portalu, a nie domyślny Bootstrap. |
| `templates/admin/base.html` | Prawdziwe menu zamiast przykładowego („Zamówienia”, „Ustawienia”): Dashboard, Placówki, Użytkownicy, Karty, Aktywacje wpłat; aktywna pozycja według `request.endpoint`. |
| `templates/panel/base.html` | Menu modułów placówki + przełącznik placówki z `g.user["shelters"]`. |

Dalszy szlif panelu (dashboardy z wykresami, ikony, dopracowane puste stany) jest w M10 i może wypaść, jeśli zabraknie czasu.

**Gotowe, gdy:**
- `/`, `/styleguide`, `/login` i `/register` (z M1) wyglądają jak makiety na telefonie (375 px) i na komputerze,
- żaden szablon nie ma własnego `<style>`, a kolory pochodzą wyłącznie z `tokens.css`,
- `/admin` i pusty panel placówki używają wspólnego szkieletu i kolorów portalu.

---

## M1. Konta i logowanie

**Cel:** rejestracja, logowanie, profil, pierwszy administrator, podstawowa moderacja kont.
**Decyzje:** R1, R2, R15, D3. **Zależy od:** M0.

**Operacje** (`operations/identity/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `RegisterUserCommand` | `email: str, password: str, first_name: str, last_name: str, phone: str = ""` → `int` | Unikalny e-mail; hasło min. 8 znaków; hash przez `generate_password_hash`. |
| `LoginUserQuery` | `email: str, password: str` → `dict \| None` | Tylko `status = 'Active'`; `check_password_hash`. |
| `GetCurrentUserQuery` | `user_id: int` → `dict \| None` | Do `g.user`: `id`, imię, `is_admin`, `status` i lista `shelters` (`id`, `name`, `status`, `is_manager`) z `shelter_employees`. Lista jest pusta do M2. |
| `GetMyProfileQuery` | `user_id: int` | |
| `UpdateMyProfileCommand` | `user_id: int, first_name: str, last_name: str, phone: str = ""` | Bez zmiany e-maila i hasła. |
| `ListUsersQuery` | `search: str = "", status: str = "", page: int = 1, limit: int = 20` | Admin; szukanie po e-mailu, imieniu i nazwisku. |
| `GetUserQuery` | `user_id: int` | Admin; z liczbą zgłoszeń, wpłat i placówek (uzupełniane w kolejnych milestone'ach). |
| `BlockUserCommand` | `actor_id: int, user_id: int, reason: str` | Na razie tylko `users`. Zamykanie zgłoszeń (R4) dochodzi w M5, M6 i M7. Nie można zablokować samego siebie. |
| `UnblockUserCommand` | `actor_id: int, user_id: int` | |
| `MakeAdminCommand` | `email: str` | Tylko z konsoli: `python test.py MakeAdminCommand --email ...` (R1). |
| `SetUserPasswordCommand` | `email: str, password: str` | Tylko z konsoli, zamiast odzyskiwania hasła (R2). |

Do tego `operations/demo/SeedDemoDataCommand.py` z kontami: administrator, 2 pracowników, 3 zwykłych użytkowników.

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /register` | `public/auth/register_form.py` | `public/auth/register.html` |
| `POST /register` | `public/auth/register.py` | → `/login` |
| `GET /login` | `public/auth/login_form.py` | `public/auth/login.html` |
| `POST /login` | `public/auth/login.py` | → `next` albo `/` |
| `POST /logout` | `public/auth/logout.py` | → `/` |
| `GET /account/profile` | `account/profile/show.py` | `account/profile.html` |
| `POST /account/profile` | `account/profile/update.py` | → `/account/profile` |
| `GET /admin/users` | `admin/users/list.py` | `admin/users/list.html` |
| `GET /admin/users/<id>` | `admin/users/details.py` | `admin/users/details.html` |
| `POST /admin/users/<id>/block` | `admin/users/block.py` | → szczegóły |
| `POST /admin/users/<id>/unblock` | `admin/users/unblock.py` | → szczegóły |

Plus `routes/auth/session.py`: `before_request` ładuje `g.user` przez `GetCurrentUserQuery` (własne krótkie połączenie tylko do odczytu). Przy `status <> 'Active'` czyści sesję. Logowanie: `session.clear()`, potem `session["user_id"] = id`.

**Gotowe, gdy:**
- można się zarejestrować (telefon opcjonalny, BR-050), zalogować i wylogować oraz edytować profil,
- `python test.py MakeAdminCommand --email ...` daje dostęp do `/admin`,
- zablokowany użytkownik zostaje wylogowany i nie może się zalogować,
- `/account/*` bez logowania przekierowuje na `/login`, a `/admin/*` dla zwykłego konta daje 403.

---

## M2. Schroniska

**Cel:** zgłoszenie placówki, zatwierdzenie, profil publiczny, personel.
**Decyzje:** D1, R1, R3, R5, D13. **Zależy od:** M1.

**Operacje** (`operations/shelter/`, stała `VOIVODESHIPS` w `__init__.py`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `SubmitShelterRegistrationCommand` | `actor_id: int, name: str, street_address: str, postal_code: str, city: str, voivodeship: str, contact_email: str, description: str = "", adoption_rules: str = "", contact_phone: str = "", website: str = ""` → `int` | `status = 'Pending'` + wiersz w `shelter_employees` z `is_manager = 1` (D1). |
| `ListMySheltersQuery` | `user_id: int` | Placówki, w których użytkownik pracuje, ze statusem (także `Pending` / `Rejected` z powodem). Zastępuje osobne „moje zgłoszenia”. |
| `ResubmitShelterRegistrationCommand` | `actor_id: int, shelter_id: int, ...pola jak przy zgłoszeniu` | Tylko ze statusu `Rejected` → `Pending`. |
| `ListPendingShelterRegistrationsQuery` | `page: int = 1, limit: int = 20` | Admin; najstarsze najpierw. |
| `ApproveShelterRegistrationCommand` | `actor_id: int, shelter_id: int` | `Pending` → `Approved`, `decided_*`, mail do zgłaszającego. |
| `RejectShelterRegistrationCommand` | `actor_id: int, shelter_id: int, reason: str` | `Pending` → `Rejected`, mail. |
| `GetShelterForManagementQuery` | `shelter_id: int` | Panel: pełne dane do formularza i dashboardu. |
| `UpdateShelterProfileCommand` | `actor_id: int, shelter_id: int, name: str, ...pozostałe pola` | Pełna zamiana pól (formularz SSR). |
| `AssignShelterEmployeeCommand` | `actor_id: int, shelter_id: int, email: str, is_manager: bool = False` | Szuka konta po e-mailu (zamiast osobnego `FindUserByEmail`); konto musi być `Active`. |
| `RemoveShelterEmployeeCommand` | `actor_id: int, shelter_id: int, user_id: int` | Nie można usunąć ostatniego kierownika (R1). |
| `ListShelterEmployeesQuery` | `shelter_id: int, page: int = 1, limit: int = 20` | Sortowanie po nazwisku. |
| `SearchSheltersQuery` | `name: str = "", voivodeship: str = "", city: str = "", page: int = 1, limit: int = 20` | Tylko `Approved` (BR-014). |
| `GetShelterProfileQuery` | `shelter_id: int` | Publiczny, tylko `Approved`, w przeciwnym razie `None`. Sekcje „zwierzęta”, „wolontariat”, „spacery” i „wsparcie” dochodzą w kolejnych milestone'ach. |
| `ListSheltersQuery` | `status: str = "", search: str = "", page: int = 1, limit: int = 20` | Admin, wszystkie statusy. |
| `BlockShelterCommand` | `actor_id: int, shelter_id: int, reason: str` | Tylko `shelters` (D13, R5). |
| `UnblockShelterCommand` | `actor_id: int, shelter_id: int` | `Approved`, gdy `decided_at IS NOT NULL`, w przeciwnym razie `Pending`. |

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /shelters` | `public/shelters/list.py` | `public/shelters/list.html` |
| `GET /shelters/<id>` | `public/shelters/details.py` | `public/shelters/details.html` |
| `GET /account/shelters` | `account/shelters/list.py` | `account/shelters/list.html` |
| `GET /account/shelters/new` | `account/shelters/new.py` | `account/shelters/form.html` |
| `POST /account/shelters` | `account/shelters/create.py` | → lista |
| `GET /account/shelters/<id>/resubmit` | `account/shelters/resubmit_form.py` | `account/shelters/form.html` |
| `POST /account/shelters/<id>/resubmit` | `account/shelters/resubmit.py` | → lista |
| `GET /panel/shelters/<sid>` | `panel/dashboard/show.py` | `panel/dashboard.html` |
| `GET /panel/shelters/<sid>/profile` | `panel/shelter/edit.py` | `panel/shelter/edit.html` |
| `POST /panel/shelters/<sid>/profile` | `panel/shelter/update.py` | → profil |
| `GET /panel/shelters/<sid>/employees` | `panel/employees/list.py` | `panel/employees/list.html` |
| `POST /panel/shelters/<sid>/employees` | `panel/employees/assign.py` (kierownik) | → lista |
| `POST /panel/shelters/<sid>/employees/<uid>/remove` | `panel/employees/remove.py` (kierownik) | → lista |
| `GET /admin/shelters` | `admin/shelters/list.py` | `admin/shelters/list.html` |
| `GET /admin/shelters/pending` | `admin/shelters/pending.py` | `admin/shelters/pending.html` |
| `GET /admin/shelters/<id>` | `admin/shelters/details.py` | `admin/shelters/details.html` |
| `POST /admin/shelters/<id>/approve`, `/reject`, `/block`, `/unblock` | `admin/shelters/{approve,reject,block,unblock}.py` | → szczegóły |

Panel placówki ze statusem `Pending` / `Rejected` działa (można przygotowywać dane, R3), ale pokazuje baner „oczekuje na zatwierdzenie”. Placówka `Blocked` ma panel tylko do odczytu (R5).

**Gotowe, gdy:**
- ścieżka „zgłoszenie → zatwierdzenie przez administratora → placówka widoczna w katalogu” działa od początku do końca,
- wyszukiwanie po nazwie, województwie i mieście działa (BR-014),
- pracownik placówki A dostaje 403 / 404 w panelu placówki B (AC-005),
- kierownik dodaje pracownika po e-mailu i nie może usunąć ostatniego kierownika.

---

## M3. Karty zwierząt i katalog

**Cel:** karta od szkicu do publikacji, katalog z filtrami, potwierdzanie aktualności, moderacja kart.
**Decyzje:** D2, D4, D8, D10, R6, R7. **Zależy od:** M2.

**Operacje** (`operations/animal/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `CreateAnimalProfileCommand` | `actor_id: int, shelter_id: int, name: str, species: str` → `int` | `Draft`; także dla placówki `Pending` (R3). |
| `UpdateAnimalProfileCommand` | `actor_id: int, shelter_id: int, animal_id: int, name: str, species: str, sex: str, description: str, daily_needs: str, breed: str = "", size: str = "", age_min_months: int = -1, age_max_months: int = -1, temperament: str = ""` | Zmiana gatunku tylko w `Draft` (R12); spójny przedział wieku. |
| `UpdateAnimalCareRequirementsCommand` | `actor_id: int, shelter_id: int, animal_id: int, good_with_children: str, good_with_dogs: str, good_with_cats: str, special_care_required: str, activity_level: str = "", min_experience: str = "", special_care_notes: str = "", notes_to_discuss: str = ""` | Upsert; wartości `Yes / No / Unknown` (D4). |
| `AddAnimalPhotoCommand` | `actor_id: int, shelter_id: int, animal_id: int, file_path: str, alt_text: str = ""` → `int` | Plik zapisuje route (`static/uploads/animals/<uuid>.<ext>`, tylko jpg / png / webp, max 5 MB); pierwsze zdjęcie dostaje `is_main = 1`. |
| `RemoveAnimalPhotoCommand` | `shelter_id: int, animal_id: int, photo_id: int` → `str` | Nie można usunąć ostatniego zdjęcia opublikowanej karty (BR-008); zwraca `file_path`, żeby route usunął plik; gdy usunięto zdjęcie główne, główne zostaje następne. |
| `SetMainAnimalPhotoCommand` | `shelter_id: int, animal_id: int, photo_id: int` | Zerowanie i ustawienie w jednej transakcji. |
| `PublishAnimalProfileCommand` | `actor_id: int, shelter_id: int, animal_id: int` | Placówka `Approved` (RB-001); komplet danych podstawowych + ≥ 1 zdjęcie (BR-008); z `Draft` / `Withdrawn` → `Available`; ustawia `published_at` i `last_confirmed_at`. |
| `WithdrawAnimalProfileCommand` | `actor_id: int, shelter_id: int, animal_id: int, reason: str` | → `Withdrawn` + `end_animal_activity` (R7). W M3 funkcja tylko ustawia `donations_enabled = 0`. |
| `HideAnimalProfileCommand` | `actor_id: int, animal_id: int, reason: str` | Admin; tylko flaga (R6, D13). |
| `UnhideAnimalProfileCommand` | `actor_id: int, animal_id: int` | Admin. |
| `ConfirmAnimalProfileAccuracyCommand` | `actor_id: int, shelter_id: int, animal_id: int, age_min_months: int = -1, age_max_months: int = -1` | Zapisuje `last_confirmed_*` i opcjonalnie koryguje wiek (D8). |
| `SearchAnimalsQuery` | `text: str = "", shelter_id: int = 0, species: str = "", sex: str = "", sizes: str = "", voivodeship: str = "", city: str = "", age_from_months: int = -1, age_to_months: int = -1, include_in_progress: bool = False, sort: str = "published", page: int = 1, limit: int = 12` | Warunek widoczności z `common.py`; część wspólna przedziałów wieku (BR-016); sortowanie `published` / `confirmed` (BR-019); domyślnie tylko `Available` (BR-020); każdy wynik ma flagę `needs_confirmation` (BR-045). |
| `GetAnimalProfileQuery` | `animal_id: int, viewer_id: int = 0` | Publiczna karta, zdjęcia, wymagania, placówka, `needs_confirmation`. `viewer_id` służy do `is_favorite` (od M4). |
| `GetAnimalProfileForManagementQuery` | `shelter_id: int, animal_id: int` | Wszystko + lista braków blokujących publikację. |
| `ListShelterAnimalsQuery` | `shelter_id: int, text: str = "", status: str = "", species: str = "", sort: str = "updated", page: int = 1, limit: int = 20` | Także szkice i zakończone karty. |
| `ListAnimalsForModerationQuery` | `search: str = "", hidden_only: bool = False, page: int = 1, limit: int = 20` | Admin, wszystkie placówki. |

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /` | `public/home/show.py` (rozbudowa) | `public/home.html`: wyszukiwarka + najnowsze karty |
| `GET /animals` | `public/animals/list.py` | `public/animals/list.html` |
| `GET /animals/<id>` | `public/animals/details.py` | `public/animals/details.html` |
| `GET /panel/shelters/<sid>/animals` | `panel/animals/list.py` | `panel/animals/list.html` |
| `GET /panel/shelters/<sid>/animals/new` | `panel/animals/new.py` | `panel/animals/new.html` |
| `POST /panel/shelters/<sid>/animals` | `panel/animals/create.py` | → edycja |
| `GET /panel/shelters/<sid>/animals/<aid>` | `panel/animals/details.py` | `panel/animals/details.html`: status, zdjęcia, akcje |
| `GET /panel/shelters/<sid>/animals/<aid>/edit` | `panel/animals/edit.py` | `panel/animals/edit.html` |
| `POST /panel/shelters/<sid>/animals/<aid>` | `panel/animals/update.py` | → szczegóły |
| `GET /panel/shelters/<sid>/animals/<aid>/requirements` | `panel/animals/requirements_edit.py` | `panel/animals/requirements.html` |
| `POST /panel/shelters/<sid>/animals/<aid>/requirements` | `panel/animals/requirements_update.py` | → szczegóły |
| `POST /panel/shelters/<sid>/animals/<aid>/photos` | `panel/animals/photo_add.py` | → szczegóły |
| `POST .../photos/<pid>/remove`, `.../photos/<pid>/main` | `panel/animals/photo_remove.py`, `photo_main.py` | → szczegóły |
| `POST .../animals/<aid>/publish`, `/withdraw`, `/confirm` | `panel/animals/{publish,withdraw,confirm}.py` | → szczegóły |
| `GET /admin/animals` | `admin/animals/list.py` | `admin/animals/list.html` |
| `POST /admin/animals/<id>/hide`, `/unhide` | `admin/animals/{hide,unhide}.py` | → lista |

Plus: lista zwierząt na `public/shelters/details.html` (`SearchAnimalsQuery(shelter_id=...)`, BR-017), komponent `animal_card`, a w panelu oznaczenie „wymaga potwierdzenia” na liście kart.

**Gotowe, gdy:**
- filtry gatunku, województwa, wieku i wielkości działają łącznie (AC-001, BR-016),
- karta pokazuje dane podstawowe, zdjęcie, potrzeby, placówkę, status i aktualność (AC-003),
- niezatwierdzona placówka ma szkic, ale nie może go opublikować (AC-004),
- po 30 dniach bez potwierdzenia jest ostrzeżenie, a potwierdzenie je usuwa i zapisuje osobę (AC-016, AC-017),
- ukryta i wycofana karta nie pojawia się w katalogu (BR-012).

---

## M4. Ulubione, profil warunków, dopasowanie

**Cel:** wyróżnik projektu, czyli dopasowanie z wyjaśnieniem.
**Decyzje:** D4, R9. **Zależy od:** M3.

**Operacje** (`operations/adoption/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `AddAnimalToFavoritesCommand` | `user_id: int, animal_id: int` | Tylko widoczna karta; `INSERT OR IGNORE`. |
| `RemoveAnimalFromFavoritesCommand` | `user_id: int, animal_id: int` | Idempotentne. |
| `ListMyFavoriteAnimalsQuery` | `user_id: int, page: int = 1, limit: int = 20` | Aktualny status; ukryta karta jako „niedostępna” bez szczegółów (BR-023). |
| `UpdateMyAdoptionConditionsCommand` | `user_id: int, has_children: str = "", has_dogs: str = "", has_cats: str = "", experience: str = "", activity_level: str = "", special_care_ready: str = "", additional_info: str = ""` | Upsert; `""` = brak odpowiedzi (BR-024); `questionnaire_version` ze stałej. |
| `GetMyAdoptionConditionsQuery` | `user_id: int` | |
| `EvaluateAnimalCompatibilityQuery` | `user_id: int, animal_id: int` → `{rules_version, items: [{criterion, category, explanation}], counts}` | Woła czystą funkcję `matching.evaluate`. |

**Logika dopasowania:** `operations/adoption/matching.py`, bez SQL:

- `RULES_VERSION = 1`, `CRITERIA = ["children", "dogs", "cats", "experience", "activity", "special_care"]`,
- `evaluate(profile: dict | None, requirements: dict | None) -> list[dict]`, kategorie `Match / Mismatch / NoData / NotApplicable`, wyjaśnienie po polsku dla każdej pary (BR-029),
- brak odpowiedzi albo `Unknown` → `NoData`, nigdy `Match` (BR-031),
- testy jednostkowe `tests/test_matching.py` (`unittest`, bez nowych zależności), przypadek po przypadku z tabeli „Przykładowe reguły dopasowania” w REQUIREMENTS §11.

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `POST /animals/<id>/favorite` | `account/favorites/add.py` | → `request.referrer` |
| `POST /animals/<id>/unfavorite` | `account/favorites/remove.py` | → `request.referrer` |
| `GET /account/favorites` | `account/favorites/list.py` | `account/favorites.html` |
| `GET /account/adoption-profile` | `account/adoption_profile/edit.py` | `account/adoption_profile.html` |
| `POST /account/adoption-profile` | `account/adoption_profile/update.py` | → formularz |

Na karcie zwierzęcia (`public/animals/details.py`): dla zalogowanego przycisk ulubionych i sekcja z wynikiem (komponent `compatibility`), a gdy profil jest pusty, zachęta do jego uzupełnienia. Profil nie jest wymagany do niczego poza tą sekcją (RB-019).

**Gotowe, gdy:**
- ulubione działają bez tworzenia zgłoszenia, lista jest prywatna (AC-006, BR-022),
- wynik rozróżnia 4 kategorie i podaje przyczyny, bez procentów i bez decyzji (AC-007, AC-009),
- kot u kandydata + nieznana reakcja psa na koty daje `NoData`, nie zgodność (AC-008),
- `python -m unittest tests.test_matching` przechodzi.

---

## M5. Zgłoszenia adopcyjne

**Cel:** zgłoszenie od wysłania do zakończenia adopcją.
**Decyzje:** D5, D6, D7, R7, R8, R15. **Zależy od:** M4.

**Operacje** (`operations/adoption/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `SubmitAdoptionApplicationCommand` | `user_id: int, animal_id: int, contact_name: str, contact_email: str, contact_phone: str = "", message: str = ""` → `int` | Zwierzę `Available`, widoczne (RB-003, BR-020); kopia profilu, wymagań i wyniku `matching.evaluate` + `RULES_VERSION` (D5); błąd z indeksu unikalnego → `BusinessRuleError` „Masz już otwarte zgłoszenie” (RB-008); zdarzenie + maile do kandydata i placówki (BR-043, bez ankiety w treści). |
| `ListMyAdoptionApplicationsQuery` | `user_id: int, status: str = "", page: int = 1, limit: int = 20` | |
| `GetAdoptionApplicationQuery` | `application_id: int, user_id: int = 0, shelter_id: int = 0` | Musi pasować `applicant_id = user_id` albo `shelter_id`; razem z historią. |
| `ListShelterAdoptionApplicationsQuery` | `shelter_id: int, animal_id: int = 0, status: str = "", page: int = 1, limit: int = 20` | |
| `StartAdoptionApplicationReviewCommand` | `actor_id: int, shelter_id: int, application_id: int, message: str = ""` | `Submitted` → `InContact`, zdarzenie, mail. |
| `SendAdoptionApplicationMessageCommand` | `actor_id: int, shelter_id: int, application_id: int, message: str` | Zdarzenie `Message` + mail (bez treści, tylko link). |
| `WithdrawAdoptionApplicationCommand` | `user_id: int, application_id: int, reason: str = ""` | Tylko własne i niezakończone; historia zostaje (BR-040). |
| `CloseAdoptionApplicationWithoutAdoptionCommand` | `actor_id: int, shelter_id: int, application_id: int, reason: str` | |
| `StartAnimalAdoptionProcessCommand` | `actor_id: int, shelter_id: int, animal_id: int, application_id: int = 0` | Według R8; `0` = proces poza portalem. |
| `ReopenAnimalForAdoptionCommand` | `actor_id: int, shelter_id: int, animal_id: int, reason: str` | Według R8. |
| `CompleteAnimalAdoptionCommand` | `actor_id: int, shelter_id: int, animal_id: int, adopted_at: str, application_id: int = 0, notes: str = ""` | `0` = adopcja poza portalem; `adopted_at` nie w przyszłości; wybrane zgłoszenie → `Adopted`, potem `end_animal_activity` (R7). |

**Rozbudowa wspólnego kodu:**
- `end_animal_activity`: zamyka otwarte zgłoszenia adopcyjne (`ClosedWithoutAdoption` + zdarzenie + mail „ogłoszenie zakończone”, BR-042),
- `BlockUserCommand`: zamyka aktywne zgłoszenia adopcyjne użytkownika (R4).

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /animals/<id>/apply` | `account/adoption/apply_form.py` | `public/animals/apply.html`: podgląd przekazywanych danych + wynik + informacja „to nie rezerwacja” (BR-034, BR-035) |
| `POST /animals/<id>/apply` | `account/adoption/apply.py` | → szczegóły zgłoszenia |
| `GET /account/applications` | `account/adoption/list.py` | `account/applications/list.html` |
| `GET /account/applications/<id>` | `account/adoption/details.py` | `account/applications/details.html` |
| `POST /account/applications/<id>/withdraw` | `account/adoption/withdraw.py` | → szczegóły |
| `GET /panel/shelters/<sid>/applications` | `panel/adoption/list.py` | `panel/applications/list.html` |
| `GET /panel/shelters/<sid>/applications/<id>` | `panel/adoption/details.py` | `panel/applications/details.html`: kopia odpowiedzi, wynik, historia, akcje |
| `POST .../applications/<id>/review`, `/message`, `/close` | `panel/adoption/{review,message,close}.py` | → szczegóły |
| `POST /panel/shelters/<sid>/animals/<aid>/adoption/start`, `/reopen`, `/complete` | `panel/adoption/{start_process,reopen,complete}.py` | → karta w panelu |

Szablony maili: `templates/mail/adoption_submitted_candidate.txt`, `adoption_submitted_shelter.txt`, `adoption_status_changed.txt`, `adoption_closed_animal_adopted.txt`. Historia zgłoszenia przez komponent `timeline`.

**Gotowe, gdy:**
- można wysłać zgłoszenie mimo rozbieżności (AC-010),
- drugie otwarte zgłoszenie do tego samego zwierzęcia jest blokowane (AC-011),
- zmiana profilu nie zmienia wysłanego zgłoszenia (AC-012),
- kandydat widzi tylko swoje zgłoszenia (AC-013),
- każda zmiana statusu ma autora, datę i mail (AC-014),
- adopcja usuwa zwierzę z katalogu i zamyka pozostałe zgłoszenia (AC-015),
- kandydat może wycofać zgłoszenie (AC-018),
- maile nie zawierają ankiety (AC-019).

---

## M6. Wolontariat

**Cel:** oferta, nabór i obsługa zgłoszeń.
**Decyzje:** R11, R15. **Zależy od:** M2 (można robić równolegle z M3–M5).

**Operacje** (`operations/volunteering/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `UpdateShelterVolunteeringOfferCommand` | `actor_id: int, shelter_id: int, description: str, forms_of_help: str, requirements: str = "", age_rules: str = "", onboarding_info: str = "", contact_info: str = ""` | Upsert; `forms_of_help` jako CSV → JSON; nie zmienia stanu naboru. |
| `OpenVolunteerRecruitmentCommand` | `actor_id: int, shelter_id: int` | Placówka `Approved`, oferta istnieje (RB-001). |
| `CloseVolunteerRecruitmentCommand` | `actor_id: int, shelter_id: int, reason: str = ""` | Nie zmienia istniejących zgłoszeń (R11). |
| `GetShelterVolunteeringOfferQuery` | `shelter_id: int` | Oferta + `recruitment_open`. |
| `SubmitVolunteerApplicationCommand` | `user_id: int, shelter_id: int, availability: str, contact_name: str, contact_email: str, rules_accepted: bool, age_confirmed: bool, preferred_forms: str = "", experience: str = "", message: str = "", contact_phone: str = ""` → `int` | Nabór otwarty, placówka `Approved`; oświadczenia = `True`; indeks unikalny → `BusinessRuleError` (BR-065); zdarzenie + mail do placówki. |
| `ListMyVolunteerApplicationsQuery` | `user_id: int, status: str = "", page: int = 1, limit: int = 20` | |
| `ListShelterVolunteerApplicationsQuery` | `shelter_id: int, status: str = "", page: int = 1, limit: int = 20` | |
| `GetVolunteerApplicationQuery` | `application_id: int, user_id: int = 0, shelter_id: int = 0` | Razem z historią. |
| `StartVolunteerApplicationReviewCommand` | `actor_id: int, shelter_id: int, application_id: int, message: str = ""` | → `InContact`. |
| `AcceptVolunteerApplicationCommand` | `actor_id: int, shelter_id: int, application_id: int, instructions: str` | → `Accepted`, mail z instrukcjami. |
| `RejectVolunteerApplicationCommand` | `actor_id: int, shelter_id: int, application_id: int, reason: str` | Powód w zdarzeniu. |
| `WithdrawVolunteerApplicationCommand` | `user_id: int, application_id: int, reason: str = ""` | Tylko aktywne. |
| `SendVolunteerApplicationMessageCommand` | `actor_id: int, shelter_id: int, application_id: int, message: str` | |
| `EndVolunteerCooperationCommand` | `actor_id: int, shelter_id: int, application_id: int, reason: str` | `Accepted` → `Ended`. |

**Rozbudowa:** `BlockUserCommand` zamyka aktywne zgłoszenia wolontariackie (R4).

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /shelters/<id>/volunteering` | `public/volunteering/offer.py` | `public/volunteering/offer.html` |
| `GET /shelters/<id>/volunteering/apply` | `account/volunteering/apply_form.py` | `public/volunteering/apply.html`: podgląd danych i wymagań (BR-063) |
| `POST /shelters/<id>/volunteering/apply` | `account/volunteering/apply.py` | → szczegóły |
| `GET /account/volunteering` | `account/volunteering/list.py` | `account/volunteering/list.html` |
| `GET /account/volunteering/<id>` | `account/volunteering/details.py` | `account/volunteering/details.html` |
| `POST /account/volunteering/<id>/withdraw` | `account/volunteering/withdraw.py` | → szczegóły |
| `GET /panel/shelters/<sid>/volunteering` | `panel/volunteering/offer_edit.py` | `panel/volunteering/offer.html` |
| `POST /panel/shelters/<sid>/volunteering` | `panel/volunteering/offer_update.py` | → oferta |
| `POST .../volunteering/open`, `/close` | `panel/volunteering/{open,close}.py` | → oferta |
| `GET /panel/shelters/<sid>/volunteering/applications` | `panel/volunteering/list.py` | `panel/volunteering/applications.html` |
| `GET .../volunteering/applications/<id>` | `panel/volunteering/details.py` | `panel/volunteering/application.html` |
| `POST .../applications/<id>/review`, `/accept`, `/reject`, `/message`, `/end` | `panel/volunteering/{review,accept,reject,message,end}.py` | → szczegóły |

Sekcja „Wolontariat” na profilu schroniska, gdy nabór jest otwarty.

**Gotowe, gdy:**
- zgłoszenie bez profilu adopcyjnego działa (AC-029),
- można wysłać zgłoszenie do placówki z otwartym naborem i zobaczyć jego status (AC-030),
- akceptacja i odrzucenie zostawiają historię i wysyłają mail (AC-031),
- drugie aktywne zgłoszenie do tej samej placówki jest blokowane (AC-032).

---

## M7. Spacery z psami

**Cel:** termin → zgłoszenie → akceptacja → realizacja.
**Decyzje:** D11, R12. **Zależy od:** M3 (wymóg wolontariatu z M6).

**Operacje** (`operations/dog_walking/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `UpdateDogWalkingRequirementsCommand` | `actor_id: int, shelter_id: int, animal_id: int, enabled: bool, min_age: int, min_experience: str, induction_required: bool, volunteer_required: bool, additional_requirements: str = ""` | Tylko psy; wyłączenie anuluje przyszłe terminy (R12). |
| `RecordDogWalkingInductionCommand` | `actor_id: int, shelter_id: int, email: str, completed_at: str, notes: str = ""` | Szuka konta po e-mailu; jedno wdrożenie na osobę w placówce. |
| `ListDogWalkingInductionsQuery` | `shelter_id: int, page: int = 1, limit: int = 20` | |
| `PublishDogWalkingSlotCommand` | `actor_id: int, shelter_id: int, animal_id: int, starts_at: str, ends_at: str, meeting_point: str, instructions: str = ""` → `int` | Placówka `Approved`, pies widoczny, spacery włączone; termin w przyszłości; kolizja psa (zapytanie z erd.md, RB-022). |
| `UpdateDogWalkingSlotCommand` | `actor_id: int, shelter_id: int, slot_id: int, starts_at: str, ends_at: str, meeting_point: str, instructions: str = ""` | Tylko `Open`; ponowne sprawdzenie kolizji. |
| `SearchDogWalkingSlotsQuery` | `shelter_id: int = 0, animal_id: int = 0, voivodeship: str = "", city: str = "", date_from: str = "", date_to: str = "", sort: str = "starts_asc", page: int = 1, limit: int = 20` | Tylko `Open`, przyszłe, widoczne. |
| `GetDogWalkingSlotQuery` | `slot_id: int` | Publiczne, bez danych kandydatów. |
| `ListShelterDogWalkingSlotsQuery` | `shelter_id: int, animal_id: int = 0, status: str = "", date_from: str = "", date_to: str = "", page: int = 1, limit: int = 20` | Z liczbą zgłoszeń; termin przeterminowany bez wyniku oznaczony „czeka na wynik” (D10). |
| `ApplyForDogWalkingSlotCommand` | `user_id: int, slot_id: int, contact_name: str, contact_email: str, declared_experience: str, age_confirmed: bool, requirements_accepted: bool, contact_phone: str = "", message: str = ""` → `int` | Termin `Open` i przyszły; indeks unikalny → `BusinessRuleError`; mail do placówki. |
| `ListMyDogWalkingApplicationsQuery` | `user_id: int, status: str = "", date_from: str = "", date_to: str = "", page: int = 1, limit: int = 20` | Razem z terminem. |
| `ListDogWalkingApplicationsQuery` | `shelter_id: int, slot_id: int, status: str = "", page: int = 1, limit: int = 20` | |
| `AcceptDogWalkingApplicationCommand` | `actor_id: int, shelter_id: int, application_id: int` | Wdrożenie / wolontariat, gdy wymagane; kolizja spacerów użytkownika (AC-037); wybrane → `Accepted`, pozostałe → `SlotTaken`, termin → `Reserved`; maile. Indeks unikalny chroni przed równoczesną akceptacją (AC-036). |
| `RejectDogWalkingApplicationCommand` | `actor_id: int, shelter_id: int, application_id: int, reason: str` | |
| `WithdrawDogWalkingApplicationCommand` | `user_id: int, application_id: int, reason: str = ""` | Najpóźniej 2 h przed `starts_at` (R12); gdy było `Accepted`, termin → `Vacated` + mail do placówki. |
| `ReopenDogWalkingSlotCommand` | `actor_id: int, shelter_id: int, slot_id: int` | `Vacated` → `Open`, termin przyszły, pies dalej dopuszczony; nie reaktywuje starych zgłoszeń (RB-023). |
| `CancelDogWalkingSlotCommand` | `actor_id: int, shelter_id: int, slot_id: int, reason: str` | Aktywne zgłoszenia → `CancelledByShelter` + maile. |
| `RecordDogWalkingOutcomeCommand` | `actor_id: int, shelter_id: int, slot_id: int, outcome: str, notes: str = ""` | Tylko `Reserved` i po `ends_at`; `Completed` / `NoShow` w terminie i zgłoszeniu. |

**Rozbudowa:** `end_animal_activity` anuluje przyszłe terminy (`cancelled_by = NULL`); `BlockUserCommand` zamyka zgłoszenia na spacery i ustawia `Vacated` (R4). Parsowanie `datetime-local` (czas polski) → UTC w helperze `routes/panel/walks/__init__.py`.

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /walks` | `public/walks/list.py` | `public/walks/list.html` |
| `GET /walks/<id>` | `public/walks/details.py` | `public/walks/details.html` |
| `GET /walks/<id>/apply` | `account/walks/apply_form.py` | `public/walks/apply.html` |
| `POST /walks/<id>/apply` | `account/walks/apply.py` | → `/account/walks` |
| `GET /account/walks` | `account/walks/list.py` | `account/walks/list.html` |
| `POST /account/walks/<app_id>/withdraw` | `account/walks/withdraw.py` | → lista |
| `GET /panel/shelters/<sid>/animals/<aid>/walking` | `panel/walks/requirements_edit.py` | `panel/walks/requirements.html` |
| `POST /panel/shelters/<sid>/animals/<aid>/walking` | `panel/walks/requirements_update.py` | → karta w panelu |
| `GET /panel/shelters/<sid>/walks` | `panel/walks/list.py` | `panel/walks/list.html` |
| `GET /panel/shelters/<sid>/walks/new` | `panel/walks/new.py` | `panel/walks/form.html` |
| `POST /panel/shelters/<sid>/walks` | `panel/walks/create.py` | → szczegóły |
| `GET /panel/shelters/<sid>/walks/<slot_id>` | `panel/walks/details.py` | `panel/walks/details.html`: termin + zgłoszenia |
| `GET` / `POST .../walks/<slot_id>/edit` | `panel/walks/{edit,update}.py` | `panel/walks/form.html` |
| `POST .../walks/<slot_id>/reopen`, `/cancel`, `/outcome` | `panel/walks/{reopen,cancel,outcome}.py` | → szczegóły |
| `POST .../walks/applications/<app_id>/accept`, `/reject` | `panel/walks/{accept,reject}.py` | → szczegóły terminu |
| `GET` / `POST /panel/shelters/<sid>/inductions` | `panel/walks/{inductions_list,induction_record}.py` | `panel/walks/inductions.html` |

Terminy psa na karcie zwierzęcia i na profilu schroniska.

**Gotowe, gdy:** spełnione AC-033 … AC-041, w tym równoczesna akceptacja (test: dwa wywołania `AcceptDogWalkingApplicationCommand` dla różnych zgłoszeń tego samego terminu; drugie kończy się `BusinessRuleError`).

---

## M8. Wsparcie finansowe

**Cel:** konfiguracja → płatność testowa → potwierdzenie → historia i statystyki.
**Decyzje:** D12, D13, R10. **Zależy od:** M3.

**Operator płatności:** wybór prawdziwego operatora jest otwarty (REQUIREMENTS Q13), a do odbioru wystarcza środowisko testowe. Dlatego:
- `payments/__init__.py`: interfejs `create_payment(donation_id, amount, return_url) -> (provider_payment_id, redirect_url)` i `verify_webhook(request) -> dict` (zdarzenie znormalizowane do pól `ApplyPaymentStatusUpdateCommand`),
- `payments/fake.py`: **fałszywy operator** w tej samej aplikacji: strona `/fake-operator/pay/<provider_payment_id>` z przyciskami „Zapłać”, „Odrzuć”, „Zwróć 50%”, „Zwróć całość”, które wysyłają na webhook zdarzenie podpisane HMAC z `SECRET_KEY`,
- prawdziwy operator to później tylko nowy moduł w `payments/`, bez zmian w operacjach.

**Operacje** (`operations/donation/`)

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `ConfigureShelterDonationSettingsCommand` | `actor_id: int, shelter_id: int, recipient_name: str, provider_recipient_id: str, suggested_amounts: str, min_amount: int, terms_text: str, support_contact: str, fees_info: str = "", max_amount: int = 0, allow_custom_amount: bool = True` | Kierownik; upsert; kwoty w groszach (CSV); zmiana `terms_text` podbija `terms_version`. |
| `GetDonationSettingsQuery` | `shelter_id: int` | Panel i admin. |
| `EnableShelterDonationsCommand` | `actor_id: int, shelter_id: int` | Tylko admin; placówka `Approved`, ustawienia kompletne (BR-055). |
| `DisableShelterDonationsCommand` | `actor_id: int, shelter_id: int, reason: str` | Kierownik albo admin; nie dotyka rozpoczętych płatności. |
| `ListDonationActivationRequestsQuery` | `page: int = 1, limit: int = 20` | Admin: placówki ze skonfigurowanymi, ale niewłączonymi wpłatami. |
| `SetAnimalDonationAvailabilityCommand` | `actor_id: int, shelter_id: int, animal_id: int, enabled: bool` | Włączenie tylko dla `Available` / `AdoptionInProgress`. |
| `SetShelterDonationStatisticsVisibilityCommand` | `actor_id: int, shelter_id: int, public: bool` | |
| `GetDonationOptionsQuery` | `shelter_id: int, animal_id: int = 0` | Odbiorca, zasady, prowizje, kwoty, `available` (warunki D13). |
| `StartDonationCommand` | `user_id: int, shelter_id: int, amount: int, animal_id: int = 0` → `int` | Warunki D13; kwota w limitach; kopia `recipient_name` i `terms_version`; `Pending`. |
| `SetDonationProviderPaymentCommand` | `donation_id: int, provider_payment_id: str` | Wołany przez route zaraz po `payments.create_payment`, w tej samej transakcji. |
| `ApplyPaymentStatusUpdateCommand` | `provider_event_id: str, provider_payment_id: str, status: str, refunded_amount: int, occurred_at: str` | `INSERT OR IGNORE` do `payment_events`; zdarzenie już znane → koniec bez zmian (AC-025); spóźnione zdarzenie nie cofa statusu; pierwsze `Succeeded` ustawia `confirmed_at`. |
| `GetDonationStatusQuery` | `user_id: int, donation_id: int` | Tylko właściciel. |
| `ListMyDonationsQuery` | `user_id: int, status: str = "", page: int = 1, limit: int = 20` | Data, kwota, odbiorca, cel, status, zwrot (BR-057). |
| `ListShelterDonationsQuery` | `shelter_id: int, status: str = "", animal_id: int = 0, date_from: str = "", date_to: str = "", page: int = 1, limit: int = 20` | Bez danych instrumentu płatniczego (BR-058). |
| `GetShelterDonationStatisticsQuery` | `shelter_id: int, date_from: str = "", date_to: str = "", public_only: bool = True` | Zapytanie z erd.md; `public_only` + `stats_public = 0` → `None`. |
| `GetAnimalDonationStatisticsQuery` | `animal_id: int, date_from: str = "", date_to: str = "", public_only: bool = True` | Jak wyżej. |
| `ExpireStalePendingDonationsCommand` | `older_than_hours: int = 24` | `Pending` → `Cancelled` (R10); z konsoli albo z crona. |

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /donate` (`?shelter_id=&animal_id=`) | `account/donations/start_form.py` | `public/donations/start.html`: kwota, odbiorca, cel, zasady (AC-022) |
| `POST /donate` | `account/donations/start.py` | → `redirect_url` operatora |
| `GET /donations/<id>/return` | `account/donations/return_page.py` | `public/donations/return.html`: tylko pokazuje bieżący status, **nie potwierdza** (AC-024) |
| `POST /payments/webhook` | `public/payments/webhook.py` (`csrf.exempt`, weryfikacja podpisu) | — |
| `GET /fake-operator/pay/<ppid>` | `public/payments/fake_pay.py` | `public/donations/fake_operator.html` |
| `POST /fake-operator/pay/<ppid>` | `public/payments/fake_action.py` | → strona powrotu |
| `GET /account/donations` | `account/donations/list.py` | `account/donations/list.html` |
| `GET /account/donations/<id>` | `account/donations/details.py` | `account/donations/details.html` |
| `GET /panel/shelters/<sid>/donations` | `panel/donations/list.py` | `panel/donations/list.html`: lista z filtrami + statystyki |
| `GET` / `POST /panel/shelters/<sid>/donations/settings` | `panel/donations/{settings_edit,settings_update}.py` | `panel/donations/settings.html` |
| `POST .../donations/disable`, `/visibility` | `panel/donations/{disable,visibility}.py` | → ustawienia |
| `POST /panel/shelters/<sid>/animals/<aid>/donations` | `panel/donations/animal_toggle.py` | → karta w panelu |
| `GET /admin/donations/activations` | `admin/donations/activations.py` | `admin/donations/activations.html` |
| `POST /admin/shelters/<sid>/donations/enable` | `admin/donations/enable.py` | → aktywacje |

Przycisk „Nakarm psiaka” na karcie psa i „Wesprzyj” na innych kartach oraz na profilu schroniska (BR-052). Nowy komponent `donation_stats` (dopisany do `components/` i `/styleguide`) w obu miejscach, gdy statystyki są publiczne.

**Gotowe, gdy:**
- spełnione AC-021 … AC-028,
- dwukrotne wysłanie tego samego zdarzenia przez fałszywego operatora nie zmienia statystyk,
- wpłata nie zmienia statusu adopcji ani zgłoszeń (AC-042).

---

## M9. Prywatność, moderacja, zadania systemowe

**Cel:** domknięcie operacji przekrojowych, które wymagają wszystkich modułów.
**Decyzje:** D3, R4, R13, R14. **Zależy od:** M5–M8.

**Operacje**

| Klasa | `execute(...)` | Reguły |
|---|---|---|
| `DeleteUserAccountCommand` (`identity/`) | `user_id: int` | Warunki blokujące z R13; bez historii `DELETE`, z historią anonimizacja (D3). Route wymaga ponownego podania hasła (`LoginUserQuery`). |
| `AnonymizeUserAccountCommand` (`identity/`) | `actor_id: int, user_id: int, reason: str` | Admin; D3 + czyszczenie kopii kontaktu we wszystkich `*_applications`. |
| `SendAnimalProfileAccuracyRemindersCommand` (`animal/`) | `threshold_days: int = 30` | Jeden zbiorczy mail na placówkę, nie częściej niż co 7 dni (`last_reminder_at`, BR-046). Z konsoli albo z crona. |
| `GetAdminDashboardQuery` (`admin/`) | — | Liczba placówek `Pending`, aktywacji wpłat, ukrytych kart, zablokowanych kont. |
| `GetShelterDashboardQuery` (`shelter/`) | `shelter_id: int` | Nowe zgłoszenia (adopcja, wolontariat, spacery), karty do potwierdzenia, najbliższe terminy, terminy czekające na wynik. |
| `BlockUserCommand` | — | Przegląd: kaskada R4 obejmuje wszystkie trzy rodzaje zgłoszeń; test z konsoli na danych demo. |

**Routes**

| Metoda i ścieżka | Plik w `routes/` | Szablon |
|---|---|---|
| `GET /account/delete` | `account/profile/delete_form.py` | `account/delete.html` |
| `POST /account/delete` | `account/profile/delete.py` | → `/` (wylogowanie) |
| `POST /admin/users/<id>/anonymize` | `admin/users/anonymize.py` | → szczegóły |
| `GET /admin` | `admin/dashboard/show.py` | `admin/dashboard.html` |
| `GET /panel/shelters/<sid>` | `panel/dashboard/show.py` (rozbudowa) | `panel/dashboard.html` |

**Gotowe, gdy:**
- usunięcie konta z historią wpłat anonimizuje dane, a statystyki się nie zmieniają (BR-051),
- przypomnienie wysłane dwa razy w tym samym tygodniu daje jeden mail,
- blokada konta i placówki działa zgodnie z R4 i R5 (BR-048),
- żaden widok publiczny ani mail nie ujawnia ankiet ani danych innych osób (AC-019; przegląd szablonów).

---

## M10. Dane demo i odbiór

**Cel:** zakres demonstracyjny z REQUIREMENTS §20 i przegląd kryteriów akceptacji.

**Zadania:**
1. `SeedDemoDataCommand`: 3–5 placówek (w tym jedna `Pending` i jedna `Blocked`), 30–50 kart psów i kotów z różnymi statusami i zdjęciami, konta wszystkich ról, zgłoszenia adopcyjne i wolontariackie w każdym statusie, terminy spacerów (przyszłe, zarezerwowane, zakończone), wpłaty potwierdzone, nieudane, częściowo i całkowicie zwrócone. Dane fikcyjne (BR-047).
2. **Testy** `tests/` (`unittest`, baza SQLite w pamięci ładowana z `schema.sql`): dopasowanie (M4), indeksy unikalne (RB-008, BR-065, AC-036), kolizje terminów, deduplikacja webhooka, kaskady `CompleteAnimalAdoption` / `WithdrawAnimalProfile` / `BlockUser`.
3. **Przegląd mobilny** (AC-020): wyszukiwarka, karta, profil warunków, zgłoszenia, rozpoczęcie wpłaty w szerokości 375 px.
4. **Szlif wyglądu**:
   - strona klienta: spójność odstępów, stany pustych list i błędów, dostępność (kontrast, `alt` zdjęć, etykiety pól, nawigacja klawiaturą),
   - panel i admin (opcjonalnie, jeśli zostanie czas): dashboardy z kafelkami i prostymi wykresami (np. wpłaty w czasie), ikony w menu, dopracowane tabele na telefonie.
5. **Lista kontrolna** AC-001 … AC-042 przejściem po danych demo (tabela poniżej), poprawki.
6. Aktualizacja `README.md` projektu: uruchomienie, `SECRET_KEY`, `MakeAdminCommand`, `SeedDemoDataCommand`, zadania z crona.

---

## Kryteria akceptacji → milestone

| AC | Milestone | AC | Milestone | AC | Milestone |
|---|---|---|---|---|---|
| 001 Wyszukiwanie | M3 | 015 Adopcja | M5 | 029 Brak profilu adopcyjnego | M6, M7, M8 |
| 002 Profil schroniska | M2, M3 | 016 Nieaktualna karta | M3 | 030 Formularz wolontariatu | M6 |
| 003 Karta zwierzęcia | M3 | 017 Potwierdzenie aktualności | M3 | 031 Obsługa wolontariatu | M6 |
| 004 Zatwierdzenie placówki | M2, M3 | 018 Wycofanie zgłoszenia | M5 | 032 Duplikaty wolontariatu | M6 |
| 005 Uprawnienia pracowników | M2 (każdy kolejny) | 019 Brak ujawnienia danych | M5, M9 | 033 Publikacja spaceru | M7 |
| 006 Ulubione | M4 | 020 Telefon | M10 | 034 Nakładanie terminów psa | M7 |
| 007 Kategorie dopasowania | M4 | 021 Wybór wsparcia | M8 | 035 Zgłoszenie na spacer | M7 |
| 008 Brak danych | M4 | 022 Jasny odbiorca i cel | M8 | 036 Limit akceptacji | M7 |
| 009 Wyjaśnienie | M4 | 023 Aktywacja płatności | M8 | 037 Konflikt terminów użytkownika | M7 |
| 010 Zgłoszenie mimo rozbieżności | M5 | 024 Potwierdzanie płatności | M8 | 038 Rezygnacja | M7 |
| 011 Duplikaty zgłoszeń | M5 | 025 Brak podwójnego naliczania | M8 | 039 Anulowanie spaceru | M7 |
| 012 Zachowanie odpowiedzi | M5 | 026 Historia wpłat | M8 | 040 Wpływ adopcji | M5, M7, M8 |
| 013 Prywatność zgłoszeń | M5 | 027 Statystyki wsparcia | M8 | 041 Zmiana zarezerwowanego spaceru | M7 |
| 014 Historia statusów | M5 | 028 Zwroty | M8 | 042 Rozdzielenie form pomocy | M8 |