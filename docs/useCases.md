Rozpisałbym to na **use case’y** nazwane po angielsku jako konkretne działania biznesowe, np. `SubmitAdoptionApplication`, a nie ogólne `AnimalService` czy techniczne `SaveAnimalToDatabase`.

W podejściu heksagonalnym są to operacje warstwy aplikacyjnej, dostępne przez porty wejściowe. Kontroler HTTP, komenda CLI czy obsługa komunikatu są adapterami wywołującymi te operacje — nie samymi use case’ami. [manning](https://www.manning.com/preview/clean-applications-with-hexagonal-architecture/chapter-4)

Poniżej kompletna mapa na podstawie naszych wymagań, w proponowanej kolejności implementacji.

- `C` — command: zmienia stan.
- `Q` — query: odczytuje dane.
- Numer oznacza kolejność na liście, nie obowiązkowy osobny etap projektu.
- Podział na commands i queries jest propozycją organizacji kodu, nie wymogiem samego heksagonu. [tsh](https://tsh.io/blog/hexagonal-architecture)

## 1. Konta użytkowników — `Identity`

Podstawa dla pozostałych modułów.

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 1 | C | `RegisterUser` | Rejestruje konto użytkownika. |
| 2 | Q | `GetMyProfile` | Pobiera profil zalogowanego użytkownika. |
| 3 | C | `UpdateMyProfile` | Aktualizuje imię i dane kontaktowe użytkownika. |
| 4 | C | `BlockUser` | Blokuje konto z podaniem powodu. |
| 5 | C | `DeleteUserAccount` | Trwale usuwa konto użytkownika na jego żądanie. |
| 6 | C | `AnonymizeUserAccount` | Anonimizuje dane osobowe przy zachowaniu historii transakcji wymaganych przez politykę przechowywania. |

Logowanie, wylogowanie, hashowanie haseł i odzyskiwanie dostępu możecie obsłużyć mechanizmami bezpieczeństwa Symfony. Nie trzeba na siłę implementować ich jako własnych biznesowych command handlerów.

`DeleteUserAccount` wymaga sprawdzenia braku aktywnych zgłoszeń adopcyjnych, wolontariackich i spacerów. `AnonymizeUserAccount` zachowuje historię wpłat i innych transakcji wymaganych przez politykę przechowywania danych, ale usuwa dane umożliwiające identyfikację osoby.

## 2. Schroniska — `Shelter`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 5 | C | `SubmitShelterRegistration` | Zgłasza nową placówkę do zatwierdzenia. |
| 6 | Q | `ListPendingShelterRegistrations` | Pokazuje administratorowi zgłoszenia oczekujące na decyzję. |
| 7 | C | `ApproveShelterRegistration` | Zatwierdza placówkę. |
| 8 | C | `RejectShelterRegistration` | Odrzuca zgłoszenie z powodem. |
| 9 | C | `UpdateShelterProfile` | Zmienia opis, adres, kontakt i zasady adopcji. |
| 10 | C | `AssignShelterEmployee` | Przypisuje istniejące konto pracownika do placówki. |
| 11 | C | `RemoveShelterEmployee` | Odbiera pracownikowi dostęp do placówki. |
| 12 | Q | `ListShelterEmployees` | Pobiera listę pracowników placówki. |
| 13 | Q | `SearchShelters` | Wyszukuje placówki po nazwie i lokalizacji. |
| 14 | Q | `GetShelterProfile` | Pobiera publiczny profil placówki. |
| 15 | C | `BlockShelter` | Blokuje placówkę i wyłącza możliwość rozpoczynania nowych działań zgodnie z wymaganiami. |

`AssignShelterEmployee` powinno działać wyłącznie dla uprawnionego administratora lub innej jawnie określonej roli — użytkownik nie może sam przypisać się do dowolnego schroniska.

## 3. Karty zwierząt — `Animal`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 16 | C | `CreateAnimalProfile` | Tworzy szkic karty zwierzęcia w placówce. |
| 17 | C | `UpdateAnimalProfile` | Aktualizuje podstawowe dane, charakter i opis. |
| 18 | C | `UpdateAnimalCareRequirements` | Zapisuje uporządkowane potrzeby i wymagania używane również przy dopasowaniu. |
| 19 | C | `AddAnimalPhoto` | Dodaje zdjęcie do karty. |
| 20 | C | `RemoveAnimalPhoto` | Usuwa zdjęcie z zachowaniem reguł publikacji. |
| 21 | C | `PublishAnimalProfile` | Publikuje kartę po sprawdzeniu kompletności i uprawnień placówki. |
| 22 | C | `WithdrawAnimalProfile` | Wycofuje zwierzę z publicznej oferty. |
| 23 | C | `HideAnimalProfile` | Ukrywa kartę administracyjnie z powodem. |
| 24 | C | `ConfirmAnimalProfileAccuracy` | Potwierdza aktualność danych i dostępności. |
| 25 | Q | `SearchAnimals` | Wyszukuje i sortuje publiczne karty według filtrów. |
| 26 | Q | `GetAnimalProfile` | Pobiera publiczną kartę zwierzęcia. |
| 27 | Q | `GetAnimalProfileForManagement` | Pobiera kartę wraz z informacjami potrzebnymi pracownikowi do zarządzania. |
| 28 | Q | `ListShelterAnimals` | Pobiera zwierzęta placówki, również szkice i karty zakończone. |

Nie dodawałbym ogólnego `ChangeAnimalStatus`, które pozwala ustawić dowolną wartość. Publikacja, wycofanie i adopcja mają różne znaczenie oraz skutki, więc powinny mieć osobne operacje.

## 4. Ulubione i profil warunków — `Adoption`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 29 | C | `AddAnimalToFavorites` | Dodaje zwierzę do ulubionych użytkownika. |
| 30 | C | `RemoveAnimalFromFavorites` | Usuwa zwierzę z ulubionych. |
| 31 | Q | `ListMyFavoriteAnimals` | Zwraca ulubione zwierzęta wraz z aktualnym statusem. |
| 32 | C | `UpdateMyAdoptionConditions` | Zapisuje lub zmienia odpowiedzi o warunkach adopcyjnych. |
| 33 | Q | `GetMyAdoptionConditions` | Pobiera zapisane odpowiedzi. |
| 34 | Q | `EvaluateAnimalCompatibility` | Porównuje warunki użytkownika z wymaganiami zwierzęcia i zwraca wyjaśnienia. |

`EvaluateAnimalCompatibility` może być query, jeśli tylko oblicza wynik i niczego nie zapisuje. Nie musi tworzyć trwałego „rekordu dopasowania” przy każdym otwarciu strony.

Stan odpowiedzi i wynik potrzebny do historii zapisujecie przy wysłaniu zgłoszenia adopcyjnego.

## 5. Adopcje — `Adoption`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 35 | C | `SubmitAdoptionApplication` | Wysyła zgłoszenie z kopią odpowiedzi, wymagań i wyniku dopasowania. |
| 36 | Q | `ListMyAdoptionApplications` | Pokazuje użytkownikowi jego zgłoszenia. |
| 37 | Q | `GetAdoptionApplication` | Pobiera szczegóły zgłoszenia po sprawdzeniu dostępu. |
| 38 | Q | `ListShelterAdoptionApplications` | Pokazuje pracownikowi zgłoszenia do jego placówki. |
| 39 | C | `StartAdoptionApplicationReview` | Oznacza zgłoszenie jako „w kontakcie”. |
| 40 | C | `SendAdoptionApplicationMessage` | Przekazuje kandydatowi krótką informację dotyczącą zgłoszenia. |
| 41 | C | `WithdrawAdoptionApplication` | Pozwala kandydatowi wycofać niezakończone zgłoszenie. |
| 42 | C | `CloseAdoptionApplicationWithoutAdoption` | Kończy zgłoszenie bez adopcji. |
| 43 | C | `StartAnimalAdoptionProcess` | Ustawia zwierzęciu status „proces adopcyjny w toku”. |
| 44 | C | `ReopenAnimalForAdoption` | Przywraca dostępność, gdy proces adopcyjny nie zakończył się adopcją. |
| 45 | C | `CompleteAnimalAdoption` | Rejestruje adopcję przez portal albo poza nim. |

### Co obejmuje `CompleteAnimalAdoption`?

To jeden proces biznesowy, który powinien doprowadzić do:

- oznaczenia zwierzęcia jako adoptowanego;
- zakończenia wybranego zgłoszenia adopcją, jeżeli takie istnieje;
- zamknięcia pozostałych niezakończonych zgłoszeń;
- wyłączenia nowych wpłat wskazujących to zwierzę;
- anulowania przyszłych spacerów;
- zainicjowania odpowiednich powiadomień.

Nie oznacza to, że cały kod musi znajdować się w jednym wielkim handlerze. Handler koordynuje proces, a reguły pozostają w odpowiednich obiektach i modułach.

## 6. Wsparcie finansowe — `Donation`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 46 | C | `ConfigureShelterDonationSettings` | Zapisuje zasady wsparcia i konfigurację odbiorcy przez uprawnioną osobę. |
| 47 | C | `EnableShelterDonations` | Włącza wpłaty po sprawdzeniu konfiguracji i gotowości odbiorcy. |
| 48 | C | `DisableShelterDonations` | Wyłącza rozpoczynanie nowych wpłat dla placówki. |
| 49 | C | `SetAnimalDonationAvailability` | Włącza lub wyłącza wsparcie wskazanego zwierzęcia, jeśli jego karta i placówka spełniają warunki. |
| 50 | C | `SetShelterDonationStatisticsVisibility` | Określa, czy statystyki wsparcia mają być publiczne. |
| 51 | Q | `GetDonationOptions` | Pokazuje cel, odbiorcę, zasady, walutę i dostępne kwoty przed płatnością. |
| 52 | C | `StartDonation` | Tworzy zamiar wpłaty i rozpoczyna płatność u operatora. |
| 53 | C | `ApplyPaymentStatusUpdate` | Przetwarza zweryfikowaną zmianę statusu płatności, w tym zwrot. |
| 54 | Q | `GetDonationStatus` | Pozwala sprawdzić bieżący stan własnej wpłaty. |
| 55 | Q | `ListMyDonations` | Pobiera historię wpłat użytkownika. |
| 56 | Q | `ListShelterDonations` | Pobiera wpłaty placówki z filtrami po dacie, statusie i zwierzęciu. |
| 57 | Q | `GetShelterDonationStatistics` | Zwraca statystyki placówki bez podwójnego liczenia. |
| 58 | Q | `GetAnimalDonationStatistics` | Zwraca statystyki wpłat wskazujących konkretne zwierzę. |

### Ważne rozdzielenie

- `StartDonation` — użytkownik chce zapłacić.
- `ApplyPaymentStatusUpdate` — operator przekazuje wynik.
- `GetDonationStatus` — użytkownik sprawdza rezultat.

Przekierowanie użytkownika z bramki płatniczej nie powinno samo uruchamiać „potwierdzenia wpłaty”.

Webhook jest adapterem wejściowym, a klient API operatora — adapterem wyjściowym. Use case nie powinien nazywać się np. `HandleStripeWebhook`, bo wiązałoby to język aplikacji z konkretnym dostawcą.

## 7. Wolontariat — `Volunteering`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 59 | C | `UpdateShelterVolunteeringOffer` | Zapisuje opis form pomocy, wymagań i wdrożenia. |
| 60 | C | `OpenVolunteerRecruitment` | Otwiera przyjmowanie zgłoszeń. |
| 61 | C | `CloseVolunteerRecruitment` | Zamyka nabór bez usuwania historii. |
| 62 | Q | `GetShelterVolunteeringOffer` | Pokazuje publiczną ofertę i aktualny stan naboru. |
| 63 | C | `SubmitVolunteerApplication` | Wysyła zgłoszenie z dostępnością, doświadczeniem i danymi kontaktowymi. |
| 64 | Q | `ListMyVolunteerApplications` | Pobiera zgłoszenia użytkownika. |
| 65 | Q | `ListShelterVolunteerApplications` | Pobiera zgłoszenia skierowane do placówki. |
| 66 | Q | `GetVolunteerApplication` | Pobiera szczegóły zgłoszenia po sprawdzeniu uprawnień. |
| 67 | C | `StartVolunteerApplicationReview` | Oznacza zgłoszenie jako „w kontakcie”. |
| 68 | C | `AcceptVolunteerApplication` | Akceptuje zgłoszenie i zapisuje dalsze instrukcje. |
| 69 | C | `RejectVolunteerApplication` | Odrzuca zgłoszenie. |
| 70 | C | `WithdrawVolunteerApplication` | Wycofuje aktywne zgłoszenie na żądanie użytkownika. |

Nie tworzyłbym jeszcze `AssignVolunteerShift`, `CalculateVolunteerHours` ani `GenerateVolunteerAgreement`, bo pełne zarządzanie wolontariatem zostawiliśmy poza MVP.

## 8. Spacery z psami — `DogWalking`

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 71 | C | `UpdateDogWalkingRequirements` | Określa możliwość spacerów z psem oraz wymagania wobec uczestników. |
| 72 | C | `PublishDogWalkingSlot` | Publikuje termin dla jednego psa i jednej osoby. |
| 73 | Q | `SearchDogWalkingSlots` | Pokazuje dostępne przyszłe terminy, np. według placówki, psa i daty. |
| 74 | Q | `GetDogWalkingSlot` | Pobiera szczegóły terminu i wymagania. |
| 75 | Q | `ListShelterDogWalkingSlots` | Pokazuje pracownikowi terminy placówki wraz ze statusami. |
| 76 | C | `ApplyForDogWalkingSlot` | Wysyła zgłoszenie na otwarty termin. |
| 77 | Q | `ListMyDogWalkingApplications` | Pokazuje zgłoszenia użytkownika i ich statusy. |
| 78 | Q | `ListDogWalkingApplications` | Pokazuje pracownikowi zgłoszenia na wskazany termin. |
| 79 | C | `AcceptDogWalkingApplication` | Akceptuje jedną osobę, sprawdza konflikty i zamyka pozostałe oczekujące zgłoszenia. |
| 80 | C | `RejectDogWalkingApplication` | Odrzuca konkretne zgłoszenie. |
| 81 | C | `WithdrawDogWalkingApplication` | Wycofuje przyszłe zgłoszenie na żądanie użytkownika. |
| 82 | C | `ReopenDogWalkingSlot` | Ponownie otwiera termin po rezygnacji uczestnika. |
| 83 | C | `CancelDogWalkingSlot` | Anuluje termin i powiadamia zainteresowanych. |
| 84 | C | `RecordDogWalkingOutcome` | Zapisuje wykonanie spaceru albo nieobecność uczestnika. |

### Gdzie pilnować reguł?

W szczególności:

- `PublishDogWalkingSlot` — brak nakładających się terminów tego samego psa.
- `AcceptDogWalkingApplication` — najwyżej jedna zaakceptowana osoba i brak konfliktu z jej innymi spacerami.
- `ReopenDogWalkingSlot` — termin nadal jest przyszły, a pies nadal może uczestniczyć.
- `RecordDogWalkingOutcome` — wynik zapisuje pracownik po planowanym terminie.

To powinny być reguły aplikacji i domeny, nie tylko walidacja przycisków we frontendzie.

## 9. Operacje uruchamiane przez system

Nie wszystko rozpoczyna użytkownik. Harmonogram i komunikaty również mogą wywoływać operacje aplikacyjne przez adaptery wejściowe. [chakray](https://chakray.com/hexagonal-architecture-a-complete-guide-to-robust-and-testable-software-design/)

| # | Typ | Nazwa use case’a | Co robi |
|---|---|---|---|
| 85 | C | `SendAnimalProfileAccuracyReminders` | Wysyła placówkom zbiorcze przypomnienia o niepotwierdzonych kartach, z ograniczeniem częstotliwości. |

Pozostałe powiadomienia mogą być reakcjami na zdarzenia, np.:

```text
AdoptionApplicationSubmitted
AdoptionApplicationStatusChanged
AnimalAdopted

DonationConfirmed
DonationRefunded

VolunteerApplicationSubmitted
VolunteerApplicationStatusChanged

DogWalkingApplicationAccepted
DogWalkingApplicationWithdrawn
DogWalkingSlotCancelled
```

To propozycje nazw zdarzeń, nie dodatkowe publiczne use case’y.

Nie potrzeba osobnego `MarkAnimalProfileAsOutdated`, jeśli informację o nieaktualności wyliczacie z daty ostatniego potwierdzenia. Nie potrzeba też cronowego „potwierdzania odbycia spaceru” — to działanie pracownika.

## 10. Jak to przełożyć na strukturę projektu?

Proponowany, prosty układ:

```text
src/
├── Identity/
├── Shelter/
├── Animal/
├── Adoption/
├── Donation/
├── Volunteering/
└── DogWalking/
```

W każdym module:

```text
Adoption/
├── Domain/
│   ├── Model/
│   ├── Event/
│   └── Repository/
│
├── Application/
│   ├── Command/
│   │   └── SubmitAdoptionApplication/
│   │       ├── SubmitAdoptionApplicationCommand.php
│   │       └── SubmitAdoptionApplicationHandler.php
│   │
│   ├── Query/
│   │   └── GetAdoptionApplication/
│   │       ├── GetAdoptionApplicationQuery.php
│   │       ├── GetAdoptionApplicationHandler.php
│   │       └── AdoptionApplicationView.php
│   │
│   └── Port/
│       └── Out/
│
└── Infrastructure/
    ├── Http/
    ├── Persistence/
    └── Messaging/
```

Przykładowy przepływ:

```text
POST /animals/{animalId}/adoption-applications
    ↓
Kontroler HTTP
    ↓
SubmitAdoptionApplicationCommand
    ↓
SubmitAdoptionApplicationHandler
    ↓
Model domenowy + porty wyjściowe
    ↓
Adapter bazy danych / adapter powiadomień
```

Kontrakt commandu i handlera może pełnić rolę wejścia aplikacyjnego. Nie musicie dodawać osobnego interfejsu do każdej klasy wyłącznie po to, żeby „było heksagonalnie”.

## 11. Co nie powinno być osobnym biznesowym use case’em?

Nie traktowałbym jako kolejnych use case’ów:

```text
SaveAnimalToDatabase
FlushEntityManager
UploadFileToS3
SendEmailUsingMailer
VerifyWebhookSignature
RenderAnimalPage
ValidateRequest
```

To operacje techniczne adapterów, implementacji portów lub walidacji wejścia. Use case powinien mówić, co aplikacja robi dla użytkownika albo procesu biznesowego, a nie jakiej technologii używa. [manning](https://www.manning.com/preview/clean-applications-with-hexagonal-architecture/chapter-4)

Podobnie nie twórzcie osobnego use case’a dla każdego filtra: `SearchAnimals` przyjmuje kryteria, zamiast rozbijać się na `SearchAnimalsByAge`, `SearchAnimalsBySize` i wszystkie ich kombinacje.

## 12. Kolejność wdrażania

Żeby nie budować przez miesiąc samych fundamentów, realizujcie kompletne ścieżki:

1. Konta → rejestracja schroniska → zatwierdzenie.
2. Utworzenie zwierzęcia → publikacja → wyszukiwanie → karta.
3. Ulubione → profil warunków → dopasowanie.
4. Zgłoszenie adopcyjne → obsługa → zakończenie adopcji.
5. Oferta wolontariatu → zgłoszenie → decyzja.
6. Termin spaceru → zgłoszenie → akceptacja → realizacja.
7. Konfiguracja wpłat → płatność testowa → potwierdzenie → historia i statystyki.
8. Przypomnienia, moderacja, scenariusze błędów i testy przekrojowe.

Konfigurację operatora i sprawdzenie możliwości przyjmowania wpłat przez schroniska warto rozpocząć równolegle wcześniej. Sama lista ma 85 operacji, ale nie oznacza 85 rozbudowanych funkcji — wiele query i prostych commandów będzie niewielkich; najwięcej uwagi wymagają adopcja, płatności i akceptowanie spacerów.