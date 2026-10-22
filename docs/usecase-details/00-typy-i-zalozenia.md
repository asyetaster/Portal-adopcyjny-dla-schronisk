# Proponowane kontrakty wejściowe use case’ów Dogsy

Źródło: projektowy `useCases.md`. To propozycja projektowa parametrów, nie odtworzenie istniejącego kodu. Dokument źródłowy podaje nazwy i zachowanie, ale nie komplet formularzy, enumów ani modelu danych. Wszystkie dodatkowe pola, warianty i wartości poniżej wymagają zatwierdzenia przy implementacji.

## Zakres

9 plików odpowiada 9 grupom operacji z dokumentu (dwie grupy Adoption pozostają osobno). Łącznie 87 use case’ów: 6 + 11 + 13 + 6 + 11 + 13 + 12 + 14 + 1. W źródle napisano 85, ale po dodaniu DeleteUserAccount i AnonymizeUserAccount numeracja ponownie zaczyna się od 5 w Shelter. Żadnej z tych operacji nie pominięto. Sekcje 10–12 źródła opisują architekturę i wdrażanie, nie kolejne grupy operacji.

## Jak czytać typy

- Kontrakty mają składnię zbliżoną do PHP: `string`, `int`, `bool`, `DateTimeImmutable`, `T|null`. `list<T>` opisuje listę w PHPDoc, a nie natywną składnię PHP. Nazwane DTO i enumy poniżej są propozycjami klas PHP.
- `x: T` — wymagane; `x: T|null = null` — opcjonalne; `—` — brak biznesowych parametrów. `= {}` oznacza DTO filtrów z domyślnymi wartościami, nie dowolną tablicę.
- Każde `...Id` jest osobnym typem value object zawierającym UUID (na granicy HTTP: string). Nie należy mieszać UserId, AnimalId itd. Format UUID jest propozycją, nie wymaganiem źródła.
- Typy złożone to immutable DTO/value objects, nie encje ORM. Parametry dotyczą wejścia; dokument nie definiuje odpowiedzi query ani typów wynikowych handlerów.
- Parametry bez domyślnej wartości są wymagane nawet wtedy, gdy sam typ dopuszcza null.

## Kontekst wykonania, nie pola formularza

Każdy handler ma zaufany `ActorContext`: `AnonymousActor`, `UserActor(userId: UserId)` albo `SystemActor(processName: NonEmptyString)`. Kontekst tworzy adapter uwierzytelnienia lub zaufany proces. Nie wolno przyjmować od klienta actorId, isAdmin, listy ról lub dowolnego userId dla operacji My. Kontrola dostępu i zakres schroniska należą do aplikacji; sam ActorContext nie dowodzi uprawnienia do zasobu.

Clock, repozytoria, transakcje, magazyn plików, polityki retencji i konfiguracja są zależnościami handlera, nie parametrami commandu. ID nowych zasobów, czasy audytu, odbiorców powiadomień, wynik dopasowania i skutki zmian wyznacza backend. `adoptedAt` jest wyjątkiem: historyczna data biznesowa adopcji.

`RegisterUser` i publiczne query dopuszczają anonimowy kontekst. StartDonation i formularze zgłoszeń zakładają konto użytkownika. Jeśli wpłaty anonimowe mają być obsługiwane, wymagają osobnej decyzji o kontrakcie i bezpiecznym dostępie do statusu. `ApplyPaymentStatusUpdate` przyjmuje wyłącznie dane zweryfikowane przez adapter operatora.

## Wspólne typy podstawowe

```text
NonEmptyString = string, po trim niepusty; limit długości zależy od pola
EmailAddress = string zweryfikowany jako adres e-mail
PhoneNumber = string znormalizowany, nie int
Url = string, zweryfikowany URL HTTPS
LocalDate = string YYYY-MM-DD, bez strefy czasowej
LocalTime = string HH:mm
TimeZoneId = string, identyfikator IANA
PositiveInt = int > 0
NonNegativeInt = int >= 0
PositiveDecimal = string reprezentujący liczbę dziesiętną > 0
Currency = string, kod ISO 4217; MVP może dopuścić wyłącznie PLN
IdempotencyKey = NonEmptyString, unikalny w zakresie użytkownika i operacji
DateTimeImmutable = moment z jawną strefą/offsetem; przechowywany jako UTC
PageRequest = {page: PositiveInt = 1, perPage: PositiveInt = 20}, perPage <= 100
DateTimeRange = {from: DateTimeImmutable|null = null, to: DateTimeImmutable|null = null}
  granice [from, to), jeśli obie istnieją: from < to
Address = {street: string|null, buildingNumber: NonEmptyString,
  apartmentNumber: string|null, postalCode: NonEmptyString, city: NonEmptyString,
  countryCode: string} // kod kraju ISO 3166-1 alpha-2
ContactDetails = {email: EmailAddress, phone: PhoneNumber|null}
GeoSearch = {latitude: float, longitude: float, radiusKm: PositiveDecimal}
  latitude [-90,90], longitude [-180,180]; sensowny limit promienia
Money = {amountMinor: PositiveInt, currency: Currency} // np. 1000 = 10,00 PLN
UploadedImage = {stream: resource, originalName: NonEmptyString,
  declaredMimeType: string|null} // resource opisany PHPDoc; treść i rozmiar weryfikuje backend
```

## Aktualizacja częściowa

`PatchField<T> = Unchanged | Set(value: T)`. W HTTP brak klucza oznacza Unchanged, a jawne null oznacza Set(null) tylko dla typu dopuszczającego null. Dzięki temu nie gubimy różnicy między „nie zmieniaj telefonu” a „usuń telefon”. Pozostałe DTO, jeśli nie mają Patch w nazwie, oznaczają pełną zamianę danych.

```text
UserProfilePatch = {
 firstName: PatchField<NonEmptyString>, lastName: PatchField<NonEmptyString>,
 phone: PatchField<PhoneNumber|null>
}
ShelterProfilePatch = {
 name: PatchField<NonEmptyString>, description: PatchField<string>,
 address: PatchField<Address>, contact: PatchField<ContactDetails>,
 adoptionRules: PatchField<string>, website: PatchField<Url|null>
}
AnimalProfilePatch = {
 name: PatchField<NonEmptyString>, species: PatchField<AnimalSpecies>,
 sex: PatchField<AnimalSex>, breed: PatchField<string|null>,
 birthDate: PatchField<LocalDate|null>, birthDateEstimated: PatchField<bool>,
 size: PatchField<AnimalSize|null>, weightKg: PatchField<PositiveDecimal|null>,
 description: PatchField<string>, temperament: PatchField<list<TemperamentTag>>
}
```

Zmiana gatunku wymaga kontroli zależnych danych (np. terminów spacerów); można ją ograniczyć wyłącznie do szkicu. Nie wyliczamy wieku jako trwałego pola wejściowego; wynika z daty urodzenia, która może być orientacyjna. Tagi opisują publiczny charakter; informacje weterynaryjne wrażliwe/niepubliczne wymagają osobnej decyzji modelowej.

## Typy Animal i Adoption — proponowany wspólny słownik dopasowania

```text
AnimalSpecies = enum {Dog, Cat, Other}
AnimalSex = enum {Male, Female, Unknown}
AnimalSize = enum {Small, Medium, Large}
TemperamentTag = enum {Calm, Active, Shy, Sociable, Independent}
AnimalProfileStatus = enum {Draft, Published, Withdrawn, Hidden, AdoptionInProgress, Adopted}
Compatibility = enum {Compatible, Incompatible, Unknown}
HousingType = enum {Apartment, House, Other}
ExperienceLevel = enum {None, Basic, Experienced}
AnimalCareRequirements = {
 allowedHousingTypes: list<HousingType>, requiresGarden: bool,
 maxHoursAlonePerDay: int|null, childrenCompatibility: Compatibility,
 dogsCompatibility: Compatibility, catsCompatibility: Compatibility,
 minimumExperience: ExperienceLevel, careNotes: string
}
AdoptionConditions = {
 housingType: HousingType, hasGarden: bool,
 hoursAwayPerDay: int, hasChildren: bool, hasDogs: bool, hasCats: bool,
 experience: ExperienceLevel, canMeetSpecialCareNeeds: bool, additionalInfo: string
}
  liczby godzin: 0..24; null w wymaganiach = brak ustalonego limitu;
  allowedHousingTypes musi być niepuste; Unknown nie oznacza Compatible.
AdoptionApplicationStatus = enum {Submitted, InContact, Withdrawn, ClosedWithoutAdoption, Adopted}
AdoptionCompletion = PortalAdoption | ExternalAdoption
PortalAdoption = {applicationId: AdoptionApplicationId, adoptedAt: DateTimeImmutable,
  notes: string|null = null}
ExternalAdoption = {adoptedAt: DateTimeImmutable, notes: string|null = null}
```

Pytania profilu i wymagania są przykładowe: źródło nie definiuje ankiety. Przed implementacją trzeba ustalić reguły oceny, interpretację braku danych i wersjonowanie ankiety. Stan odpowiedzi, wymagań i wyniku utrwalany jest przy wysłaniu zgłoszenia. Po stronie klienta nie ma parametru compatibilityScore. AdoptionInProgress jako stan karty to uproszczenie; implementacja może rozdzielić widoczność karty od dostępności adopcyjnej.

## Typy Donation

```text
DonationTarget = ShelterTarget {shelterId: ShelterId} | AnimalTarget {animalId: AnimalId}
StatisticsVisibility = enum {Public, StaffOnly}
PaymentProvider = NonEmptyString // identyfikator skonfigurowanego adaptera
ProviderRecipientId = NonEmptyString
ShelterDonationSettings = {
 provider: PaymentProvider, recipientId: ProviderRecipientId, currency: Currency,
 suggestedAmountsMinor: list<PositiveInt>, minimumAmountMinor: PositiveInt,
 maximumAmountMinor: PositiveInt|null, allowCustomAmount: bool,
 termsText: NonEmptyString, termsVersion: NonEmptyString
}
DonationStatus = enum {Pending, Processing, Succeeded, Failed, Cancelled,
  PartiallyRefunded, Refunded}
PaymentStatus = enum {Pending, Processing, Succeeded, Failed, Cancelled,
  PartiallyRefunded, Refunded}
VerifiedPaymentUpdate = {
 provider: PaymentProvider, providerEventId: NonEmptyString,
 providerPaymentId: NonEmptyString, status: PaymentStatus,
 amount: Money, refundedTotalMinor: NonNegativeInt,
 occurredAt: DateTimeImmutable
}
```

DonationTarget jest sumą rozłączną: nie można podać jednocześnie dowolnego schroniska i obcego zwierzęcia. Schronisko dla AnimalTarget wynika z bazy. Parametry kwot konfiguracyjnych muszą być spójne z minimum, maksimum i walutą. Money nie korzysta z float. W VerifiedPaymentUpdate `amount` oznacza oryginalną kwotę płatności, a `refundedTotalMinor` skumulowany zwrot, nie przyrost. Adapter musi znormalizować to z API operatora; backend kojarzy płatność po provider + providerPaymentId, deduplikuje zdarzenia i nie cofa stanu na podstawie spóźnionego webhooka. Kontrakt wymaga uzgodnienia z wybranym operatorem, zwłaszcza częściowych zwrotów i kolejności zdarzeń. Jeżeli operator nie podaje wiarygodnej sumy zwrotów, adapter ją uzgadnia albo potrzebny jest osobny kontrakt pojedynczego zwrotu z jego ID.

## Typy Volunteering i DogWalking

```text
VolunteeringOffer = {
 description: NonEmptyString, formsOfHelp: list<NonEmptyString>,
 requirements: string, onboardingInstructions: string
}
VolunteerAvailability = {
 timeZone: TimeZoneId, weeklyWindows: list<WeeklyTimeWindow>, notes: string|null
}
WeeklyTimeWindow = {dayOfWeek: int, startsAt: LocalTime, endsAt: LocalTime}
  dayOfWeek 1..7, startsAt < endsAt, okna nie przechodzą przez północ;
  co najmniej jedno okno lub niepusta notatka opisująca dostępność
VolunteerApplicationStatus = enum {Submitted, InContact, Accepted, Rejected, Withdrawn}
DogWalkingRequirements = {
 enabled: bool, minimumAge: int, minimumExperience: ExperienceLevel,
 inductionRequired: bool, additionalRequirements: string
}
  minimumAge 0..120; konkretne minimum wynika z ustalonej polityki placówki
DogWalkingParticipantDeclaration = {
 birthDate: LocalDate, experience: ExperienceLevel,
 requirementsAcknowledged: bool
}
DogWalkingSlotStatus = enum {Open, Reserved, AwaitingOutcome, Completed,
  ParticipantNoShow, Cancelled}
DogWalkingApplicationStatus = enum {Pending, Accepted, Rejected, Withdrawn, Closed}
DogWalkingOutcome = enum {Completed, ParticipantNoShow}
```

Potwierdzenie zapoznania się z wymaganiami nie jest zgodą marketingową i musi mieć wartość true przy wysyłce. Wdrożenie/szkolenie powinno być zweryfikowane w zaufanych danych placówki, nie przez flagę isTrained od kandydata. Data urodzenia jest propozycją do sprawdzania wieku; trzeba ustalić minimalny niezbędny zakres danych i retencję. AwaitingOutcome może być stanem wyliczanym z czasu, a nie zapisywanym.

## Filtry i sortowanie

Wszystkie pola filtrów są opcjonalne, z domyślnym null lub pustą listą. Pusta lista oznacza brak danego ograniczenia. Sortowanie to zamknięte enumy mapowane na bezpieczne pola, nigdy surowe nazwy kolumn SQL.

```text
ShelterSearchFilters = {name: string|null = null, city: string|null = null,
 geo: GeoSearch|null = null}
AnimalSearchFilters = {text: string|null = null, shelterId: ShelterId|null = null,
 species: AnimalSpecies|null = null, sex: AnimalSex|null = null,
 sizes: list<AnimalSize> = [], minAgeMonths: NonNegativeInt|null = null,
 maxAgeMonths: NonNegativeInt|null = null, city: string|null = null,
 geo: GeoSearch|null = null}
ShelterAnimalFilters = {text: string|null = null,
 statuses: list<AnimalProfileStatus> = [], species: AnimalSpecies|null = null}
AdoptionApplicationFilters = {animalId: AnimalId|null = null,
 statuses: list<AdoptionApplicationStatus> = [], submittedDuring: DateTimeRange|null = null}
DonationFilters = {statuses: list<DonationStatus> = [],
 createdDuring: DateTimeRange|null = null, animalId: AnimalId|null = null,
 currency: Currency|null = null}
DogWalkingSlotSearchFilters = {shelterId: ShelterId|null = null,
 animalId: AnimalId|null = null, startsDuring: DateTimeRange|null = null,
 city: string|null = null}
ShelterDogWalkingSlotFilters = {animalId: AnimalId|null = null,
 statuses: list<DogWalkingSlotStatus> = [], startsDuring: DateTimeRange|null = null}
ShelterRegistrationSort = enum {SubmittedAtAsc, SubmittedAtDesc}
ShelterSort = enum {NameAsc, DistanceAsc}
AnimalSort = enum {Newest, AgeAsc, AgeDesc, DistanceAsc}
AnimalManagementSort = enum {UpdatedAtDesc, NameAsc}
DogWalkingSlotSort = enum {StartsAtAsc, StartsAtDesc}
```

DistanceAsc wymaga GeoSearch. Zakresy minimum/maksimum muszą być spójne. Dla stronicowania stosuj stabilny tie-breaker po ID. Brak parametru sort w danym query oznacza ustalone sortowanie: zgłoszenia, ulubione i wpłaty od najnowszych; pracownicy po nazwisku i ID; sloty zarządcze po czasie rozpoczęcia. Zakres dat statystyk dotyczy czasu potwierdzenia wpłaty, a zwroty odejmujemy dla wybranej kohorty wpłat według aktualnego stanu. Jest to propozycja definicji metryki, nie jedyna poprawna interpretacja.

## Decyzje do zatwierdzenia

1. Dokładne pola formularzy, długości tekstów, ankieta adopcyjna i kryteria dopasowania.
2. Samoobsługowa czy wyłącznie administracyjna anonimizacja; konkretne reguły retencji.
3. Model ról pracowników, minima wieku, weryfikacja szkolenia i ograniczenia spacerów.
4. Proces adopcji poza portalem i reguły kontaktu z kandydatem.
5. Operator płatności, waluty, obsługa częściowych zwrotów i ewentualne wpłaty anonimowe.
6. Wymagalność powodów wycofania/odrzucenia dodanych jako propozycje audytowe.

To kontrakty aplikacyjne, nie gotowe schematy HTTP: adapter mapuje JSON/formularz na typy, buduje zaufany kontekst, sprawdza formaty, a aplikacja i domena egzekwują reguły biznesowe. Nie wymagają mechanicznego tworzenia osobnej klasy dla każdego drobnego typu — poziom formalizacji warto dopasować do projektu.
