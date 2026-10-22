# Adopcje — Adoption

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## SubmitAdoptionApplication (C)

```text
SubmitAdoptionApplication(
    animalId: AnimalId,
    message: string
)
```

null = null|Pobiera zapisane AdoptionConditions; backend utrwala ich kopię, kopię wymagań i sam oblicza wynik. Identyfikatory zgłoszenia, użytkownika oraz czas nie pochodzą z formularza.

## ListMyAdoptionApplications (Q)

```text
ListMyAdoptionApplications(
    statuses: list<AdoptionApplicationStatus> = [],
    page: PageRequest = default
)
```

Pusta lista oznacza wszystkie dozwolone statusy własnych zgłoszeń.

## GetAdoptionApplication (Q)

```text
GetAdoptionApplication(
    applicationId: AdoptionApplicationId
)
```

Wnioskodawca lub uprawniony pracownik.

## ListShelterAdoptionApplications (Q)

```text
ListShelterAdoptionApplications(
    shelterId: ShelterId,
    filters: AdoptionApplicationFilters = {},
    page: PageRequest = default
)
```

Zakres uprawnień sprawdzany dla placówki.

## StartAdoptionApplicationReview (C)

```text
StartAdoptionApplicationReview(
    applicationId: AdoptionApplicationId
)
```

Przejście do stanu InContact, nie dowolny status.

## SendAdoptionApplicationMessage (C)

```text
SendAdoptionApplicationMessage(
    applicationId: AdoptionApplicationId,
    message: NonEmptyString
)
```

Odbiorca wyznaczany ze zgłoszenia, nie jako dowolny userId.

## WithdrawAdoptionApplication (C)

```text
WithdrawAdoptionApplication(
    applicationId: AdoptionApplicationId,
    reason: string
)
```

null = null|Wyłącznie własne niezakończone zgłoszenie.

## CloseAdoptionApplicationWithoutAdoption (C)

```text
CloseAdoptionApplicationWithoutAdoption(
    applicationId: AdoptionApplicationId,
    reason: NonEmptyString
)
```

Pracownik zamyka bez adopcji.

## StartAnimalAdoptionProcess (C)

```text
StartAnimalAdoptionProcess(
    animalId: AnimalId,
    applicationId: AdoptionApplicationId
)
```

null = null|Założenie: możliwy też proces poza portalem. Jeśli ID podano, musi dotyczyć tego zwierzęcia.

## ReopenAnimalForAdoption (C)

```text
ReopenAnimalForAdoption(
    animalId: AnimalId,
    reason: NonEmptyString
)
```

Backend rozlicza powiązany proces i sprawdza możliwość przywrócenia.

## CompleteAnimalAdoption (C)

```text
CompleteAnimalAdoption(
    animalId: AnimalId,
    adoption: AdoptionCompletion
)
```

Wariant Portal wymaga applicationId; External go nie ma. Backend zamyka pozostałe zgłoszenia, blokuje nowe wpłaty na zwierzę, anuluje przyszłe spacery i inicjuje powiadomienia. Nie przyjmuj tych skutków jako flag klienta.
