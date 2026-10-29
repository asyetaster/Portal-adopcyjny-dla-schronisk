-- =====================================================================
-- Portal adopcyjny dla schronisk: proponowany schemat bazy (SQLite)
-- Źródło: docs/db-diagram/erd.md (diagram + sekcja 3. Ograniczenia)
--
-- Konwencje (szczegóły w docs/db-diagram/README.md):
--   * PK: INTEGER PRIMARY KEY
--   * bool: INTEGER 0/1 z CHECK
--   * enumy: TEXT z CHECK (... IN (...))
--   * daty: TEXT ISO-8601 UTC, np. '2026-10-28T12:00:00Z'
--   * kwoty: INTEGER w groszach, tylko PLN
--   * json: TEXT z json.dumps()
--   * updated_at ustawia aplikacja przy każdym UPDATE (brak triggerów)
--
-- SQLite domyślnie NIE sprawdza kluczy obcych. PRAGMA poniżej działa
-- tylko dla połączenia, które wykonuje ten skrypt. Każde połączenie
-- aplikacji musi ją ustawić samo (np. w handlerze "connect" w database.py).
-- =====================================================================

PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY,
    -- Przy anonimizacji (README, D3) e-mail zastępujemy unikalną wartością,
    -- np. 'anonymized-<id>@invalid', a imię i nazwisko wartością 'Anonim'.
    email           TEXT    NOT NULL UNIQUE COLLATE NOCASE
                            CHECK (length(email) BETWEEN 3 AND 254),
    password_hash   TEXT    NOT NULL,
    first_name      TEXT    NOT NULL CHECK (length(first_name) BETWEEN 1 AND 100),
    last_name       TEXT    NOT NULL CHECK (length(last_name) BETWEEN 1 AND 100),
    phone           TEXT,                                   -- BR-050: opcjonalny
    is_admin        INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1)),
    status          TEXT    NOT NULL DEFAULT 'Active'
                            CHECK (status IN ('Active', 'Blocked', 'Anonymized')),
    blocked_reason  TEXT,
    blocked_at      TEXT,
    blocked_by      INTEGER REFERENCES users (id),
    anonymized_at   TEXT,
    created_at      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (status <> 'Blocked'    OR blocked_reason IS NOT NULL),   -- BR-048
    CHECK (status <> 'Anonymized' OR anonymized_at  IS NOT NULL)
);


-- =====================================================================
-- Shelter
-- =====================================================================

-- Zgłoszenie placówki to od razu wiersz ze statusem 'Pending' (README, D1).
CREATE TABLE IF NOT EXISTS shelters (
    id                INTEGER PRIMARY KEY,
    name              TEXT    NOT NULL CHECK (length(name) BETWEEN 1 AND 200),
    description       TEXT    NOT NULL DEFAULT '',
    street_address    TEXT    NOT NULL,
    postal_code       TEXT    NOT NULL,
    city              TEXT    NOT NULL,
    voivodeship       TEXT    NOT NULL,                     -- BR-002, BR-014, BR-015
    contact_email     TEXT    NOT NULL,
    contact_phone     TEXT,
    website           TEXT,
    adoption_rules    TEXT    NOT NULL DEFAULT '',
    status            TEXT    NOT NULL DEFAULT 'Pending'
                              CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Blocked')),
    submitted_by      INTEGER NOT NULL REFERENCES users (id),
    submitted_at      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    decided_by        INTEGER REFERENCES users (id),
    decided_at        TEXT,
    rejection_reason  TEXT,
    blocked_reason    TEXT,
    blocked_at        TEXT,
    blocked_by        INTEGER REFERENCES users (id),
    last_reminder_at  TEXT,                                -- BR-046: max raz w tygodniu
    created_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (status <> 'Rejected' OR rejection_reason IS NOT NULL),
    CHECK (status <> 'Blocked'  OR blocked_reason   IS NOT NULL),
    CHECK (status NOT IN ('Approved', 'Rejected') OR decided_at IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS ix_shelters_search
    ON shelters (status, voivodeship, city);


CREATE TABLE IF NOT EXISTS shelter_employees (
    shelter_id   INTEGER NOT NULL REFERENCES shelters (id) ON DELETE CASCADE,
    -- Brak CASCADE na users: pracownika nie można usunąć twardo (G-14).
    user_id      INTEGER NOT NULL REFERENCES users (id),
    is_manager   INTEGER NOT NULL DEFAULT 0 CHECK (is_manager IN (0, 1)),
    assigned_by  INTEGER NOT NULL REFERENCES users (id),
    assigned_at  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    PRIMARY KEY (shelter_id, user_id)
);

CREATE INDEX IF NOT EXISTS ix_shelter_employees_user
    ON shelter_employees (user_id);                         -- ListMyShelters


-- =====================================================================
-- Animal
-- =====================================================================

CREATE TABLE IF NOT EXISTS animals (
    id                       INTEGER PRIMARY KEY,
    shelter_id               INTEGER NOT NULL REFERENCES shelters (id),
    name                     TEXT    NOT NULL CHECK (length(name) BETWEEN 1 AND 100),
    species                  TEXT    NOT NULL CHECK (species IN ('Dog', 'Cat')),
    sex                      TEXT    NOT NULL DEFAULT 'Unknown'
                                     CHECK (sex IN ('Male', 'Female', 'Unknown')),
    breed                    TEXT,
    age_min_months           INTEGER CHECK (age_min_months >= 0),   -- BR-016
    age_max_months           INTEGER CHECK (age_max_months >= 0),
    size                     TEXT    CHECK (size IN ('Small', 'Medium', 'Large')),
    description              TEXT    NOT NULL DEFAULT '',            -- charakter
    daily_needs              TEXT    NOT NULL DEFAULT '',            -- BR-007
    temperament              TEXT,                                   -- tagi CSV
    status                   TEXT    NOT NULL DEFAULT 'Draft'
                                     CHECK (status IN ('Draft', 'Available', 'AdoptionInProgress',
                                                       'Adopted', 'Withdrawn')),
    withdrawn_reason         TEXT,
    -- Moderacja niezależna od status (README, D2)
    is_hidden                INTEGER NOT NULL DEFAULT 0 CHECK (is_hidden IN (0, 1)),
    hidden_reason            TEXT,
    hidden_at                TEXT,
    hidden_by                INTEGER REFERENCES users (id),
    published_at             TEXT,                                   -- BR-019
    last_confirmed_at        TEXT,                                   -- BR-044
    last_confirmed_by        INTEGER REFERENCES users (id),
    donations_enabled        INTEGER NOT NULL DEFAULT 0 CHECK (donations_enabled IN (0, 1)),
    -- Zgłoszenie w procesie adopcyjnym albo zakończone adopcją (README, D6).
    -- Tabela adoption_applications powstaje niżej; SQLite sprawdza FK przy zapisie danych.
    adoption_application_id  INTEGER REFERENCES adoption_applications (id),
    adoption_type            TEXT    CHECK (adoption_type IN ('Portal', 'External')),
    adopted_at               TEXT,
    adoption_notes           TEXT,
    created_at               TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at               TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (age_min_months IS NULL OR age_max_months IS NULL
           OR age_min_months <= age_max_months),
    CHECK (status <> 'Withdrawn' OR withdrawn_reason IS NOT NULL),
    CHECK (is_hidden = 0 OR hidden_reason IS NOT NULL),
    CHECK (status = 'Draft' OR published_at IS NOT NULL),
    CHECK (status <> 'Adopted' OR (adopted_at IS NOT NULL AND adoption_type IS NOT NULL)),
    CHECK (adoption_type <> 'Portal' OR adoption_application_id IS NOT NULL),
    CHECK (status <> 'AdoptionInProgress' OR adoption_type IS NULL)
);

CREATE INDEX IF NOT EXISTS ix_animals_search
    ON animals (status, is_hidden, species, size);          -- SearchAnimals
CREATE INDEX IF NOT EXISTS ix_animals_shelter
    ON animals (shelter_id, status);                        -- ListShelterAnimals
CREATE INDEX IF NOT EXISTS ix_animals_last_confirmed
    ON animals (last_confirmed_at);                         -- przypomnienia, sortowanie


CREATE TABLE IF NOT EXISTS animal_care_requirements (
    animal_id              INTEGER PRIMARY KEY REFERENCES animals (id) ON DELETE CASCADE,
    -- BR-010: odpowiedź negatywna i brak informacji to różne stany
    good_with_children     TEXT    NOT NULL DEFAULT 'Unknown'
                                   CHECK (good_with_children IN ('Yes', 'No', 'Unknown')),
    good_with_dogs         TEXT    NOT NULL DEFAULT 'Unknown'
                                   CHECK (good_with_dogs IN ('Yes', 'No', 'Unknown')),
    good_with_cats         TEXT    NOT NULL DEFAULT 'Unknown'
                                   CHECK (good_with_cats IN ('Yes', 'No', 'Unknown')),
    activity_level         TEXT    CHECK (activity_level IN ('Low', 'Medium', 'High')),
    min_experience         TEXT    CHECK (min_experience IN ('None', 'Basic', 'Experienced')),
    special_care_required  TEXT    NOT NULL DEFAULT 'Unknown'
                                   CHECK (special_care_required IN ('Yes', 'No', 'Unknown')),
    special_care_notes     TEXT,
    notes_to_discuss       TEXT,                            -- BR-009
    updated_by             INTEGER NOT NULL REFERENCES users (id),
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);


CREATE TABLE IF NOT EXISTS animal_photos (
    id           INTEGER PRIMARY KEY,
    animal_id    INTEGER NOT NULL REFERENCES animals (id) ON DELETE CASCADE,
    file_path    TEXT    NOT NULL,
    alt_text     TEXT,
    position     INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    is_main      INTEGER NOT NULL DEFAULT 0 CHECK (is_main IN (0, 1)),
    uploaded_by  INTEGER NOT NULL REFERENCES users (id),
    created_at   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS ix_animal_photos_animal
    ON animal_photos (animal_id, position);
-- Jedno zdjęcie główne na zwierzę (BR-018)
CREATE UNIQUE INDEX IF NOT EXISTS ux_animal_photos_main
    ON animal_photos (animal_id) WHERE is_main = 1;


-- =====================================================================
-- Adoption
-- =====================================================================

-- Dodanie idempotentne: INSERT OR IGNORE
CREATE TABLE IF NOT EXISTS favorite_animals (
    user_id     INTEGER NOT NULL REFERENCES users (id)   ON DELETE CASCADE,
    animal_id   INTEGER NOT NULL REFERENCES animals (id) ON DELETE CASCADE,
    created_at  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    PRIMARY KEY (user_id, animal_id)
);


-- NULL w polach odpowiedzi = „bez odpowiedzi” (BR-024, BR-031). CHECK przepuszcza NULL.
CREATE TABLE IF NOT EXISTS adoption_profiles (
    user_id                INTEGER PRIMARY KEY REFERENCES users (id) ON DELETE CASCADE,
    has_children           INTEGER CHECK (has_children IN (0, 1)),
    has_dogs               INTEGER CHECK (has_dogs IN (0, 1)),
    has_cats               INTEGER CHECK (has_cats IN (0, 1)),
    experience             TEXT    CHECK (experience IN ('None', 'Basic', 'Experienced')),
    activity_level         TEXT    CHECK (activity_level IN ('Low', 'Medium', 'High')),
    special_care_ready     INTEGER CHECK (special_care_ready IN (0, 1)),
    additional_info        TEXT,
    questionnaire_version  INTEGER NOT NULL DEFAULT 1 CHECK (questionnaire_version >= 1),
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);


CREATE TABLE IF NOT EXISTS adoption_applications (
    id                     INTEGER PRIMARY KEY,
    animal_id              INTEGER NOT NULL REFERENCES animals (id),
    shelter_id             INTEGER NOT NULL REFERENCES shelters (id),   -- kopia z animals (README, D9)
    applicant_id           INTEGER NOT NULL REFERENCES users (id),
    status                 TEXT    NOT NULL DEFAULT 'Submitted'
                                   CHECK (status IN ('Submitted', 'InContact', 'Withdrawn',
                                                     'ClosedWithoutAdoption', 'Adopted')),
    message                TEXT,
    -- Kopia kontaktu z chwili wysłania (BR-034)
    contact_name           TEXT    NOT NULL,
    contact_email          TEXT    NOT NULL,
    contact_phone          TEXT,
    -- Stan z chwili wysłania jako JSON (BR-041, README, D5)
    profile_snapshot       TEXT    NOT NULL,
    requirements_snapshot  TEXT    NOT NULL,
    match_snapshot         TEXT    NOT NULL,     -- [{criterion, category, explanation}, ...]
    match_rules_version    INTEGER NOT NULL CHECK (match_rules_version >= 1),   -- BR-033
    submitted_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    closed_at              TEXT,
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    -- closed_at ustawione dokładnie wtedy, gdy zgłoszenie jest zakończone
    CHECK ((status IN ('Submitted', 'InContact')) = (closed_at IS NULL))
);

-- Najwyżej jedno niezakończone zgłoszenie osoby do zwierzęcia (RB-008, AC-011)
CREATE UNIQUE INDEX IF NOT EXISTS ux_adoption_applications_active
    ON adoption_applications (applicant_id, animal_id)
    WHERE status IN ('Submitted', 'InContact');
CREATE INDEX IF NOT EXISTS ix_adoption_applications_shelter
    ON adoption_applications (shelter_id, status, submitted_at);
CREATE INDEX IF NOT EXISTS ix_adoption_applications_animal
    ON adoption_applications (animal_id, status);


-- Historia statusów i wiadomości (BR-038). Każda zmiana status w zgłoszeniu
-- = UPDATE zgłoszenia + INSERT tutaj, w jednej transakcji.
CREATE TABLE IF NOT EXISTS adoption_application_events (
    id              INTEGER PRIMARY KEY,
    application_id  INTEGER NOT NULL REFERENCES adoption_applications (id) ON DELETE CASCADE,
    type            TEXT    NOT NULL CHECK (type IN ('StatusChange', 'Message')),
    from_status     TEXT    CHECK (from_status IN ('Submitted', 'InContact', 'Withdrawn',
                                                   'ClosedWithoutAdoption', 'Adopted')),
    to_status       TEXT    CHECK (to_status IN ('Submitted', 'InContact', 'Withdrawn',
                                                 'ClosedWithoutAdoption', 'Adopted')),
    message         TEXT,
    author_id       INTEGER REFERENCES users (id),          -- NULL = system
    created_at      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (type <> 'StatusChange' OR to_status IS NOT NULL),
    CHECK (type <> 'Message'      OR message   IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS ix_adoption_application_events_application
    ON adoption_application_events (application_id, created_at);


-- =====================================================================
-- Donation
-- =====================================================================

CREATE TABLE IF NOT EXISTS donation_settings (
    shelter_id             INTEGER PRIMARY KEY REFERENCES shelters (id) ON DELETE CASCADE,
    recipient_name         TEXT    NOT NULL,                -- BR-054
    provider_recipient_id  TEXT    NOT NULL,
    suggested_amounts      TEXT    NOT NULL DEFAULT '[]',   -- JSON, grosze: [1000, 3000, 5000]
    min_amount             INTEGER NOT NULL CHECK (min_amount > 0),
    max_amount             INTEGER,
    allow_custom_amount    INTEGER NOT NULL DEFAULT 1 CHECK (allow_custom_amount IN (0, 1)),
    terms_text             TEXT    NOT NULL,
    terms_version          INTEGER NOT NULL DEFAULT 1 CHECK (terms_version >= 1),
    support_contact        TEXT    NOT NULL,                -- BR-061
    fees_info              TEXT    NOT NULL DEFAULT '',     -- BR-054: czy prowizje zmniejszają kwotę dla odbiorcy
    enabled                INTEGER NOT NULL DEFAULT 0 CHECK (enabled IN (0, 1)),
    enabled_by             INTEGER REFERENCES users (id),   -- tylko admin, nadzór (sekcja 4.4)
    enabled_at             TEXT,
    disabled_reason        TEXT,
    disabled_at            TEXT,
    stats_public           INTEGER NOT NULL DEFAULT 0 CHECK (stats_public IN (0, 1)),   -- BR-059
    updated_by             INTEGER NOT NULL REFERENCES users (id),
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (max_amount IS NULL OR max_amount >= min_amount),
    CHECK (enabled = 0 OR (enabled_by IS NOT NULL AND enabled_at IS NOT NULL))
);


-- StartDonation sprawdza warunki przy odczycie, a nie przez zerowanie flag (README, D13):
--   shelters.status = 'Approved' AND donation_settings.enabled = 1
--   oraz dla celu "zwierzę": animals.status IN ('Available', 'AdoptionInProgress')
--   AND animals.is_hidden = 0 AND animals.donations_enabled = 1   (BR-060)
CREATE TABLE IF NOT EXISTS donations (
    id                   INTEGER PRIMARY KEY,
    user_id              INTEGER NOT NULL REFERENCES users (id),
    shelter_id           INTEGER NOT NULL REFERENCES shelters (id),
    animal_id            INTEGER REFERENCES animals (id),   -- NULL = wsparcie całej placówki
    amount               INTEGER NOT NULL CHECK (amount > 0),   -- grosze, PLN
    status               TEXT    NOT NULL DEFAULT 'Pending'
                                 CHECK (status IN ('Pending', 'Succeeded', 'Failed', 'Cancelled',
                                                   'PartiallyRefunded', 'Refunded')),
    refunded_amount      INTEGER NOT NULL DEFAULT 0,        -- skumulowana suma zwrotów
    provider_payment_id  TEXT    UNIQUE,                    -- NULL do utworzenia płatności u operatora
    recipient_name       TEXT    NOT NULL,                  -- kopia z chwili wpłaty
    terms_version        INTEGER NOT NULL,                  -- kopia z chwili wpłaty
    created_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    confirmed_at         TEXT,                              -- pierwsze Succeeded, data do statystyk
    updated_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (refunded_amount BETWEEN 0 AND amount),
    CHECK (status <> 'Refunded' OR refunded_amount = amount),
    CHECK (status <> 'PartiallyRefunded' OR refunded_amount BETWEEN 1 AND amount - 1),
    CHECK (status NOT IN ('Succeeded', 'PartiallyRefunded', 'Refunded') OR confirmed_at IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS ix_donations_user
    ON donations (user_id, created_at);                     -- ListMyDonations
CREATE INDEX IF NOT EXISTS ix_donations_shelter
    ON donations (shelter_id, status, confirmed_at);        -- panel i statystyki placówki
CREATE INDEX IF NOT EXISTS ix_donations_animal
    ON donations (animal_id, status, confirmed_at);         -- statystyki zwierzęcia


-- Deduplikacja zdarzeń operatora (AC-025): INSERT OR IGNORE; gdy nic nie
-- wstawiono, zdarzenie już było i command kończy bez zmian.
CREATE TABLE IF NOT EXISTS payment_events (
    id                 INTEGER PRIMARY KEY,
    provider_event_id  TEXT    NOT NULL UNIQUE,
    donation_id        INTEGER NOT NULL REFERENCES donations (id),
    status             TEXT    NOT NULL
                               CHECK (status IN ('Pending', 'Succeeded', 'Failed', 'Cancelled',
                                                 'PartiallyRefunded', 'Refunded')),
    refunded_amount    INTEGER NOT NULL DEFAULT 0 CHECK (refunded_amount >= 0),
    occurred_at        TEXT    NOT NULL,
    received_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS ix_payment_events_donation
    ON payment_events (donation_id, occurred_at);


-- =====================================================================
-- Volunteering
-- =====================================================================

CREATE TABLE IF NOT EXISTS volunteering_offers (
    shelter_id              INTEGER PRIMARY KEY REFERENCES shelters (id) ON DELETE CASCADE,
    description             TEXT    NOT NULL,
    forms_of_help           TEXT    NOT NULL DEFAULT '[]',  -- JSON: lista form pomocy
    requirements            TEXT    NOT NULL DEFAULT '',
    age_rules               TEXT    NOT NULL DEFAULT '',    -- BR-062
    onboarding_info         TEXT    NOT NULL DEFAULT '',
    contact_info            TEXT    NOT NULL DEFAULT '',    -- BR-062
    recruitment_open        INTEGER NOT NULL DEFAULT 0 CHECK (recruitment_open IN (0, 1)),
    recruitment_changed_at  TEXT,
    updated_by              INTEGER NOT NULL REFERENCES users (id),
    updated_at              TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);


CREATE TABLE IF NOT EXISTS volunteer_applications (
    id               INTEGER PRIMARY KEY,
    shelter_id       INTEGER NOT NULL REFERENCES shelters (id),
    applicant_id     INTEGER NOT NULL REFERENCES users (id),
    -- 'Ended' = zakończenie współpracy, propozycja z G-18
    status           TEXT    NOT NULL DEFAULT 'Submitted'
                             CHECK (status IN ('Submitted', 'InContact', 'Accepted',
                                               'Rejected', 'Withdrawn', 'Ended')),
    preferred_forms  TEXT    NOT NULL DEFAULT '[]',         -- JSON, BR-063
    availability     TEXT    NOT NULL,                      -- opis tekstowy
    experience       TEXT,
    message          TEXT,
    contact_name     TEXT    NOT NULL,
    contact_email    TEXT    NOT NULL,
    contact_phone    TEXT,
    rules_accepted   INTEGER NOT NULL CHECK (rules_accepted = 1),   -- oświadczenie BR-063
    age_confirmed    INTEGER NOT NULL CHECK (age_confirmed = 1),    -- zamiast daty urodzenia, BR-050
    instructions     TEXT,                                  -- ustawiane przy akceptacji
    submitted_at     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    closed_at        TEXT,
    updated_at       TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (status <> 'Accepted' OR instructions IS NOT NULL),
    -- Aktywne (BR-065) = Submitted, InContact, Accepted; tylko one mają closed_at = NULL
    CHECK ((status IN ('Submitted', 'InContact', 'Accepted')) = (closed_at IS NULL))
);

-- Najwyżej jedno aktywne zgłoszenie osoby do placówki (BR-065, AC-032)
CREATE UNIQUE INDEX IF NOT EXISTS ux_volunteer_applications_active
    ON volunteer_applications (applicant_id, shelter_id)
    WHERE status IN ('Submitted', 'InContact', 'Accepted');
CREATE INDEX IF NOT EXISTS ix_volunteer_applications_shelter
    ON volunteer_applications (shelter_id, status, submitted_at);


CREATE TABLE IF NOT EXISTS volunteer_application_events (
    id              INTEGER PRIMARY KEY,
    application_id  INTEGER NOT NULL REFERENCES volunteer_applications (id) ON DELETE CASCADE,
    type            TEXT    NOT NULL CHECK (type IN ('StatusChange', 'Message')),
    from_status     TEXT    CHECK (from_status IN ('Submitted', 'InContact', 'Accepted',
                                                   'Rejected', 'Withdrawn', 'Ended')),
    to_status       TEXT    CHECK (to_status IN ('Submitted', 'InContact', 'Accepted',
                                                 'Rejected', 'Withdrawn', 'Ended')),
    message         TEXT,
    author_id       INTEGER REFERENCES users (id),          -- NULL = system
    created_at      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (type <> 'StatusChange' OR to_status IS NOT NULL),
    CHECK (type <> 'Message'      OR message   IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS ix_volunteer_application_events_application
    ON volunteer_application_events (application_id, created_at);


-- =====================================================================
-- DogWalking
-- =====================================================================

CREATE TABLE IF NOT EXISTS dog_walking_requirements (
    animal_id                INTEGER PRIMARY KEY REFERENCES animals (id) ON DELETE CASCADE,
    enabled                  INTEGER NOT NULL DEFAULT 0 CHECK (enabled IN (0, 1)),
    min_age                  INTEGER NOT NULL DEFAULT 18 CHECK (min_age BETWEEN 0 AND 120),
    min_experience           TEXT    NOT NULL DEFAULT 'None'
                                     CHECK (min_experience IN ('None', 'Basic', 'Experienced')),
    induction_required       INTEGER NOT NULL DEFAULT 0 CHECK (induction_required IN (0, 1)),
    volunteer_required       INTEGER NOT NULL DEFAULT 0 CHECK (volunteer_required IN (0, 1)),   -- BR-067
    additional_requirements  TEXT,
    updated_by               INTEGER NOT NULL REFERENCES users (id),
    updated_at               TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);


-- Potwierdzenie wdrożenia przez pracownika (luka G-17)
CREATE TABLE IF NOT EXISTS dog_walking_inductions (
    id            INTEGER PRIMARY KEY,
    shelter_id    INTEGER NOT NULL REFERENCES shelters (id),
    user_id       INTEGER NOT NULL REFERENCES users (id),
    completed_at  TEXT    NOT NULL,
    recorded_by   INTEGER NOT NULL REFERENCES users (id),
    notes         TEXT,

    UNIQUE (shelter_id, user_id)
);


-- Nakładanie się terminów psa (RB-022, AC-034) sprawdza PublishDogWalkingSlot
-- w transakcji BEGIN IMMEDIATE (zapytanie w erd.md, sekcja DogWalking).
CREATE TABLE IF NOT EXISTS dog_walking_slots (
    id                   INTEGER PRIMARY KEY,
    animal_id            INTEGER NOT NULL REFERENCES animals (id),
    shelter_id           INTEGER NOT NULL REFERENCES shelters (id),   -- kopia z animals (README, D9)
    starts_at            TEXT    NOT NULL,
    ends_at              TEXT    NOT NULL,
    meeting_point        TEXT    NOT NULL,
    instructions         TEXT,
    -- 'Vacated' = po rezygnacji zaakceptowanej osoby, czeka na ReopenDogWalkingSlot (G-09)
    status               TEXT    NOT NULL DEFAULT 'Open'
                                 CHECK (status IN ('Open', 'Reserved', 'Vacated',
                                                   'Cancelled', 'Completed', 'NoShow')),
    cancel_reason        TEXT,
    cancelled_by         INTEGER REFERENCES users (id),     -- NULL przy anulowaniu przez system (adopcja, wycofanie psa)
    cancelled_at         TEXT,
    outcome_notes        TEXT,
    outcome_recorded_by  INTEGER REFERENCES users (id),
    outcome_recorded_at  TEXT,
    created_by           INTEGER NOT NULL REFERENCES users (id),
    created_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (ends_at > starts_at),
    CHECK (status <> 'Cancelled' OR (cancel_reason IS NOT NULL AND cancelled_at IS NOT NULL)),
    CHECK (status NOT IN ('Completed', 'NoShow')
           OR (outcome_recorded_by IS NOT NULL AND outcome_recorded_at IS NOT NULL))
);

CREATE INDEX IF NOT EXISTS ix_dog_walking_slots_animal
    ON dog_walking_slots (animal_id, starts_at);            -- sprawdzanie kolizji psa
CREATE INDEX IF NOT EXISTS ix_dog_walking_slots_shelter
    ON dog_walking_slots (shelter_id, starts_at);           -- ListShelterDogWalkingSlots
CREATE INDEX IF NOT EXISTS ix_dog_walking_slots_search
    ON dog_walking_slots (status, starts_at);               -- SearchDogWalkingSlots


-- Kolizję zaakceptowanych spacerów użytkownika (AC-037) sprawdza
-- AcceptDogWalkingApplication w transakcji (zapytanie w erd.md).
CREATE TABLE IF NOT EXISTS dog_walking_applications (
    id                     INTEGER PRIMARY KEY,
    slot_id                INTEGER NOT NULL REFERENCES dog_walking_slots (id),
    applicant_id           INTEGER NOT NULL REFERENCES users (id),
    -- Statusy z BR-071 + 'SlotTaken' (zamknięte po akceptacji innej osoby)
    status                 TEXT    NOT NULL DEFAULT 'Pending'
                                   CHECK (status IN ('Pending', 'Accepted', 'Rejected', 'Withdrawn',
                                                     'SlotTaken', 'CancelledByShelter',
                                                     'Completed', 'NoShow')),
    message                TEXT,
    contact_name           TEXT    NOT NULL,                -- kopia, BR-069
    contact_email          TEXT    NOT NULL,
    contact_phone          TEXT,
    age_confirmed          INTEGER NOT NULL CHECK (age_confirmed = 1),          -- zamiast daty urodzenia (G-20)
    declared_experience    TEXT    NOT NULL
                                   CHECK (declared_experience IN ('None', 'Basic', 'Experienced')),
    requirements_accepted  INTEGER NOT NULL CHECK (requirements_accepted = 1),  -- BR-069
    decision_reason        TEXT,
    decided_by             INTEGER REFERENCES users (id),
    decided_at             TEXT,
    created_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    CHECK (status <> 'Rejected' OR decision_reason IS NOT NULL)
);

-- Najwyżej jedna zaakceptowana osoba na termin, także przy równoczesnych akceptacjach (RB-021, AC-036)
CREATE UNIQUE INDEX IF NOT EXISTS ux_dog_walking_applications_accepted
    ON dog_walking_applications (slot_id)
    WHERE status = 'Accepted';
-- Jedno aktywne zgłoszenie osoby na termin (BR-069)
CREATE UNIQUE INDEX IF NOT EXISTS ux_dog_walking_applications_active
    ON dog_walking_applications (slot_id, applicant_id)
    WHERE status IN ('Pending', 'Accepted');
CREATE INDEX IF NOT EXISTS ix_dog_walking_applications_applicant
    ON dog_walking_applications (applicant_id, status);     -- ListMyDogWalkingApplications