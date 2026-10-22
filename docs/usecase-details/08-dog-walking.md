# Spacery z psami — DogWalking

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## UpdateDogWalkingRequirements (C)

```text
UpdateDogWalkingRequirements(
    animalId: AnimalId,
    requirements: DogWalkingRequirements
)
```

Backend sprawdza, że zwierzę jest psem; pełna zamiana wymagań.

## PublishDogWalkingSlot (C)

```text
PublishDogWalkingSlot(
    animalId: AnimalId,
    startsAt: DateTimeImmutable,
    endsAt: DateTimeImmutable,
    meetingPoint: NonEmptyString,
    instructions: string
)
```

null = null|Placówka wynika ze zwierzęcia. Jedno zwierzę i jedna osoba; capacity nie jest parametrem. Sprawdź przyszłość i brak kolizji psa.

## SearchDogWalkingSlots (Q)

```text
SearchDogWalkingSlots(
    filters: DogWalkingSlotSearchFilters = {},
    page: PageRequest = default,
    sort: DogWalkingSlotSort = StartsAtAsc
)
```

Tylko dostępne przyszłe terminy; zakres czasu nie omija tej reguły.

## GetDogWalkingSlot (Q)

```text
GetDogWalkingSlot(
    slotId: DogWalkingSlotId
)
```

Publiczne szczegóły bez danych osobowych kandydatów.

## ListShelterDogWalkingSlots (Q)

```text
ListShelterDogWalkingSlots(
    shelterId: ShelterId,
    filters: ShelterDogWalkingSlotFilters = {},
    page: PageRequest = default
)
```

Odczyt zarządczy ze statusami.

## ApplyForDogWalkingSlot (C)

```text
ApplyForDogWalkingSlot(
    slotId: DogWalkingSlotId,
    declaration: DogWalkingParticipantDeclaration,
    message: string
)
```

null = null|Tożsamość z ActorContext. Deklaracja nie zastępuje kontroli uprawnień, ograniczeń wieku i kolizji.

## ListMyDogWalkingApplications (Q)

```text
ListMyDogWalkingApplications(
    statuses: list<DogWalkingApplicationStatus> = [],
    period: DateTimeRange
)
```

null = null; page: PageRequest = default|Własne zgłoszenia wraz z terminami.

## ListDogWalkingApplications (Q)

```text
ListDogWalkingApplications(
    slotId: DogWalkingSlotId,
    statuses: list<DogWalkingApplicationStatus> = [],
    page: PageRequest = default
)
```

Pracownik placówki danego terminu.

## AcceptDogWalkingApplication (C)

```text
AcceptDogWalkingApplication(
    applicationId: DogWalkingApplicationId
)
```

Slot, pies i osoba wynikają ze zgłoszenia. Backend pilnuje pojedynczej akceptacji, kolizji uczestnika i zamyka pozostałe oczekujące zgłoszenia.

## RejectDogWalkingApplication (C)

```text
RejectDogWalkingApplication(
    applicationId: DogWalkingApplicationId,
    reason: NonEmptyString
)
```

Pracownik; nie zmienia dowolnie statusu slotu.

## WithdrawDogWalkingApplication (C)

```text
WithdrawDogWalkingApplication(
    applicationId: DogWalkingApplicationId,
    reason: string
)
```

null = null|Własne przyszłe zgłoszenie; otwarcie slotu pozostaje jawną operacją ReopenDogWalkingSlot.

## ReopenDogWalkingSlot (C)

```text
ReopenDogWalkingSlot(
    slotId: DogWalkingSlotId
)
```

Tylko przyszły termin po rezygnacji i przy aktualnym dopuszczeniu psa.

## CancelDogWalkingSlot (C)

```text
CancelDogWalkingSlot(
    slotId: DogWalkingSlotId,
    reason: NonEmptyString
)
```

Odbiorców powiadomień ustala backend.

## RecordDogWalkingOutcome (C)

```text
RecordDogWalkingOutcome(
    slotId: DogWalkingSlotId,
    outcome: DogWalkingOutcome,
    notes: string
)
```

null = null|Pracownik po planowanym zakończeniu; outcome = Completed albo ParticipantNoShow. Czas zapisu z Clock.
