# Wsparcie finansowe — Donation

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## ConfigureShelterDonationSettings (C)

```text
ConfigureShelterDonationSettings(
    shelterId: ShelterId,
    settings: ShelterDonationSettings
)
```

Uprawniona osoba. Identyfikator odbiorcy jest referencją do operatora, nie kluczem API. Sekrety poza commandem.

## EnableShelterDonations (C)

```text
EnableShelterDonations(
    shelterId: ShelterId
)
```

Gotowość odbiorcy sprawdzana u operatora, nie jako client-provided boolean.

## DisableShelterDonations (C)

```text
DisableShelterDonations(
    shelterId: ShelterId,
    reason: NonEmptyString
)
```

Nie unieważnia rozpoczętych płatności.

## SetAnimalDonationAvailability (C)

```text
SetAnimalDonationAvailability(
    animalId: AnimalId,
    enabled: bool
)
```

Schronisko ustalane z animalId; warunki aktywacji sprawdza backend.

## SetShelterDonationStatisticsVisibility (C)

```text
SetShelterDonationStatisticsVisibility(
    shelterId: ShelterId,
    visibility: StatisticsVisibility
)
```

Proponowany enum Public / StaffOnly.

## GetDonationOptions (Q)

```text
GetDonationOptions(
    target: DonationTarget
)
```

Rozłączny cel Shelter albo Animal; odbiorca wynika z backendu.

## StartDonation (C)

```text
StartDonation(
    target: DonationTarget,
    amount: Money,
    idempotencyKey: IdempotencyKey
)
```

Założenie MVP: wpłaty zalogowanych użytkowników. Regulamin i konfiguracja odbiorcy utrwalane przez backend. Adresy powrotu z konfiguracji, nie dowolny URL klienta.

## ApplyPaymentStatusUpdate (C)

```text
ApplyPaymentStatusUpdate(
    update: VerifiedPaymentUpdate
)
```

Wyłącznie z zaufanego adaptera po weryfikacji autentyczności; operator-neutralny kontrakt. Nigdy z przekierowania przeglądarki. Deduplikacja i uzgodnienie kwot oraz waluty po stronie backendu.

## GetDonationStatus (Q)

```text
GetDonationStatus(
    donationId: DonationId
)
```

Sprawdzenie właściciela; sam identyfikator nie daje dostępu.

## ListMyDonations (Q)

```text
ListMyDonations(
    filters: DonationFilters = {},
    page: PageRequest = default
)
```

Właściciel z ActorContext.

## ListShelterDonations (Q)

```text
ListShelterDonations(
    shelterId: ShelterId,
    filters: DonationFilters = {},
    page: PageRequest = default
)
```

Uprawniony pracownik; filtry obejmują datę, status i zwierzę.

## GetShelterDonationStatistics (Q)

```text
GetShelterDonationStatistics(
    shelterId: ShelterId,
    period: DateTimeRange
)
```

null = null; currency: Currency|null = null|Widoczność z konfiguracji; nie sumuj różnych walut. Gdy currency=null, osobne wyniki per waluta. Kwoty zwrotów liczone netto, bez dublowania zdarzeń.

## GetAnimalDonationStatistics (Q)

```text
GetAnimalDonationStatistics(
    animalId: AnimalId,
    period: DateTimeRange
)
```

null = null; currency: Currency|null = null|Te same zasady widoczności, walut i deduplikacji.
