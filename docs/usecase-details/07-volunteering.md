# Wolontariat — Volunteering

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## UpdateShelterVolunteeringOffer (C)

```text
UpdateShelterVolunteeringOffer(
    shelterId: ShelterId,
    offer: VolunteeringOffer
)
```

Pełny zestaw pól oferty; nie zmienia stanu naboru.

## OpenVolunteerRecruitment (C)

```text
OpenVolunteerRecruitment(
    shelterId: ShelterId
)
```

Warunki kompletności oferty i aktywności placówki w backendzie.

## CloseVolunteerRecruitment (C)

```text
CloseVolunteerRecruitment(
    shelterId: ShelterId,
    reason: string
)
```

null = null|Zamyka nowe zgłoszenia, zachowuje historię.

## GetShelterVolunteeringOffer (Q)

```text
GetShelterVolunteeringOffer(
    shelterId: ShelterId
)
```

Publiczna oferta i aktualny stan naboru.

## SubmitVolunteerApplication (C)

```text
SubmitVolunteerApplication(
    shelterId: ShelterId,
    availability: VolunteerAvailability,
    experience: string,
    motivation: NonEmptyString,
    contact: ContactDetails
)
```

Wnioskodawca z ActorContext. Kontakt jako kopia dla zgłoszenia; motywacja to propozycja dodatkowego pola.

## ListMyVolunteerApplications (Q)

```text
ListMyVolunteerApplications(
    statuses: list<VolunteerApplicationStatus> = [],
    page: PageRequest = default
)
```

Tylko własne zgłoszenia.

## ListShelterVolunteerApplications (Q)

```text
ListShelterVolunteerApplications(
    shelterId: ShelterId,
    statuses: list<VolunteerApplicationStatus> = [],
    page: PageRequest = default
)
```

Uprawniony pracownik.

## GetVolunteerApplication (Q)

```text
GetVolunteerApplication(
    applicationId: VolunteerApplicationId
)
```

Właściciel lub uprawniony pracownik.

## StartVolunteerApplicationReview (C)

```text
StartVolunteerApplicationReview(
    applicationId: VolunteerApplicationId
)
```

Przejście do InContact.

## AcceptVolunteerApplication (C)

```text
AcceptVolunteerApplication(
    applicationId: VolunteerApplicationId,
    instructions: NonEmptyString
)
```

Instrukcje dalszego postępowania.

## RejectVolunteerApplication (C)

```text
RejectVolunteerApplication(
    applicationId: VolunteerApplicationId,
    reason: NonEmptyString
)
```

Powód jako proponowana reguła audytu.

## WithdrawVolunteerApplication (C)

```text
WithdrawVolunteerApplication(
    applicationId: VolunteerApplicationId,
    reason: string
)
```

null = null|Wyłącznie własne aktywne zgłoszenie.
