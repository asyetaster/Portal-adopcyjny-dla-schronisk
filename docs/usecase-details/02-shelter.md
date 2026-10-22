# Schroniska — Shelter

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## SubmitShelterRegistration (C)

```text
SubmitShelterRegistration(
    name: NonEmptyString,
    description: string,
    address: Address,
    contact: ContactDetails,
    adoptionRules: string
)
```

Zgłaszający z ActorContext; nie przyjmuj statusu zatwierdzenia. Pola opisu i zasad mogą być puste na etapie zgłoszenia — decyzja produktowa.

## ListPendingShelterRegistrations (Q)

```text
ListPendingShelterRegistrations(
    page: PageRequest = default,
    sort: ShelterRegistrationSort = SubmittedAtAsc
)
```

Administrator. Status pending narzucony przez operację.

## ApproveShelterRegistration (C)

```text
ApproveShelterRegistration(
    registrationId: ShelterRegistrationId
)
```

Zatwierdzający i czas z kontekstu oraz zegara.

## RejectShelterRegistration (C)

```text
RejectShelterRegistration(
    registrationId: ShelterRegistrationId,
    reason: NonEmptyString
)
```

Administrator.

## UpdateShelterProfile (C)

```text
UpdateShelterProfile(
    shelterId: ShelterId,
    profile: ShelterProfilePatch
)
```

Sprawdź dostęp do konkretnej placówki.

## AssignShelterEmployee (C)

```text
AssignShelterEmployee(
    shelterId: ShelterId,
    userId: UserId
)
```

Przypisanie istniejącego konta; administrator lub jawnie uprawniona rola. Nie dodaję arbitralnego parametru role.

## RemoveShelterEmployee (C)

```text
RemoveShelterEmployee(
    shelterId: ShelterId,
    userId: UserId
)
```

Uprawnienia sprawdzane po stronie aplikacji.

## ListShelterEmployees (Q)

```text
ListShelterEmployees(
    shelterId: ShelterId,
    page: PageRequest = default
)
```

Lista niepubliczna.

## SearchShelters (Q)

```text
SearchShelters(
    filters: ShelterSearchFilters = {},
    page: PageRequest = default,
    sort: ShelterSort = NameAsc
)
```

Publiczny odczyt; nie pokazuje niezatwierdzonych i zablokowanych placówek.

## GetShelterProfile (Q)

```text
GetShelterProfile(
    shelterId: ShelterId
)
```

Publiczny profil.

## BlockShelter (C)

```text
BlockShelter(
    shelterId: ShelterId,
    reason: NonEmptyString
)
```

Administrator; skutki blokady wylicza aplikacja.
