# PORTAL ADOPCYJNY DLA SCHRONISK
## Wymagania biznesowe - wersja animal-centered

Wersja 0.1
Status: Draft
Główny cel: wyszukiwanie zwierząt do adopcji i wspieranie kontaktu ze schroniskami
Źródło danych: profile i karty zwierząt publikowane przez schroniska
Zakres geograficzny: Polska, z pilotażem na ograniczonej liczbie placówek  

---
## 1. Cel projektu
Celem projektu jest stworzenie portalu łączącego osoby zainteresowane adopcją zwierząt ze schroniskami.
 
Platforma ma umożliwiać:
 
- wyszukiwanie schronisk i zwierząt dostępnych do adopcji;
- poznanie potrzeb i charakteru zwierzęcia;
- porównanie potrzeb zwierzęcia z warunkami deklarowanymi przez potencjalnego opiekuna;
- przesłanie zgłoszenia zainteresowania adopcją;
- obsługę zgłoszeń przez pracowników schroniska;
- utrzymywanie aktualnych informacji o dostępności zwierząt.
 
Przykładowe pytanie biznesowe:
 
> Znajdź psy średniej wielkości, w wieku do 5 lat, w promieniu 50 km od mojego miasta, które mogą mieszkać z dziećmi.
 
Portal wspiera proces adopcyjny, ale nie podejmuje decyzji o adopcji. Decyzja pozostaje po stronie schroniska i kandydata.

---
## 2. Główna zasada produktu
 
Centralnym obiektem platformy jest zwierzę dostępne do adopcji.
 
Schronisko jest źródłem informacji o zwierzęciu oraz podmiotem odpowiedzialnym za obsługę zgłoszeń.
 
Oznacza to, że:

- zwierzę jest głównym obiektem wyszukiwania i analizy;
- schronisko, lokalizacja i zasady adopcji stanowią kontekst jego karty;
- użytkownik powinien móc szybko przejść od listy zwierząt do pełnej karty wybranego zwierzęcia;
- głównym sposobem korzystania z systemu jest wyszukiwanie i filtrowanie zwierząt;
- dopasowanie warunków ma przygotować rozmowę ze schroniskiem, a nie zastąpić decyzję schroniska;
- aktualność ogłoszenia powinna być widoczna dla użytkownika.
 
---
 
## 3. Główne zastosowania biznesowe
 
Platforma ma wspierać przede wszystkim:
 
1. wyszukiwanie zwierząt według lokalizacji i podstawowych cech;
2. przeglądanie schronisk i ich podopiecznych;
3. poznawanie potrzeb, charakteru i wymagań zwierzęcia;
4. zapisywanie interesujących zwierząt do ulubionych;
5. określanie warunków, jakie kandydat może zapewnić;
6. otrzymywanie wyjaśnienia zgodności i rozbieżności między warunkami kandydata a potrzebami zwierzęcia;
7. przesyłanie zgłoszeń zainteresowania adopcją;
8. obsługę zgłoszeń przez schroniska;
9. aktualizowanie dostępności zwierząt;
10. ograniczanie liczby nieaktualnych ogłoszeń.
 
---
 
## 4. Użytkownicy i role
 
### 4.1. Gość
 
Użytkownik niezalogowany, który może:
 
- przeglądać katalog schronisk;
- wyszukiwać zwierzęta;
- korzystać z filtrów;
- przeglądać publiczne karty zwierząt;
- zapoznawać się z zasadami adopcji.
 
### 4.2. Kandydat do adopcji
 
Użytkownik zalogowany, który dodatkowo może:
 
- zarządzać własnym profilem;
- zapisać warunki adopcyjne;
- korzystać z dopasowania z wyjaśnieniem;
- dodawać zwierzęta do ulubionych;
- wysyłać zgłoszenia;
- sprawdzać status własnych zgłoszeń i nimi zarządzać.
 
### 4.3. Pracownik schroniska
 
Użytkownik przypisany do placówki, który może:
 
- zarządzać profilem swojego schroniska;
- tworzyć i aktualizować karty zwierząt;
- określać potrzeby i wymagania zwierząt;
- zmieniać statusy dostępności;
- potwierdzać aktualność ogłoszeń;
- przeglądać i obsługiwać zgłoszenia dotyczące swojej placówki.
 
### 4.4. Administrator
 
Użytkownik odpowiedzialny za:
 
- zatwierdzanie kont schronisk;
- moderowanie ogłoszeń;
- blokowanie kont i placówek w przypadku nadużyć.
 
---
 
## 5. Główne obiekty biznesowe
 
Platforma powinna operować co najmniej na następujących obiektach:
 
- zwierzę;
- karta zwierzęcia;
- schronisko;
- konto użytkownika;
- przypisanie pracownika do schroniska;
- profil warunków adopcyjnych;
- potrzeby i wymagania zwierzęcia;
- wynik dopasowania;
- zgłoszenie zainteresowania adopcją;
- historia statusów zgłoszenia;
- lista ulubionych;
- potwierdzenie aktualności ogłoszenia.
 
W MVP obsługiwane gatunki to psy i koty.
 
---
 
## 6. Profile schronisk
 
### BR-001 — Jednoznaczny profil schroniska
 
Każde schronisko powinno posiadać jeden możliwy do jednoznacznego zidentyfikowania profil.
 
### BR-002 — Dane schroniska
 
Profil powinien zawierać:
 
- nazwę;
- opis;
- adres;
- miejscowość;
- województwo;
- publiczne dane kontaktowe;
- zasady adopcji;
- opcjonalnie adres strony internetowej.
 
### BR-003 — Rejestracja placówki
 
Przedstawiciel schroniska powinien móc zgłosić placówkę do zatwierdzenia przez administratora.
 
### BR-004 — Weryfikacja przed publikacją
 
Niezatwierdzona placówka może przygotowywać dane, ale nie może publikować publicznych kart zwierząt.
 
Administrator ręcznie weryfikuje uprawnienie przedstawiciela do prowadzenia profilu.
 
Zatwierdzenie profilu nie oznacza certyfikacji warunków opieki w placówce.
 
### BR-005 — Zarządzanie własną placówką
 
Pracownik może zarządzać wyłącznie placówką, do której został przypisany.
 
---
 
## 7. Karta zwierzęcia
 
### BR-006 — Jednoznaczna karta
 
Każde zwierzę powinno posiadać stały identyfikator, byc przypisane do jednego schroniska.
 
Zmiana opisu, zdjęć lub statusu nie może powodować utworzenia nowej karty.
 
### BR-007 — Dane podstawowe
 
Karta powinna zawierać:
 
- imię lub oznaczenie;
- gatunek;
- płeć albo informację, że jest nieustalona;
- wiek lub szacowany przedział wieku;
- wielkość;
- opis charakteru;
- opis codziennych potrzeb;
- zdjęcia;
- schronisko;
- lokalizację;
- status dostępności;
- datę ostatniego potwierdzenia aktualności.
 
### BR-008 — Warunki publikacji
 
Opublikowanie karty wymaga:
 
- przypisania do zatwierdzonej placówki;
- uzupełnienia danych podstawowych;
- dodania co najmniej jednego zdjęcia;
- określenia statusu dostępności.
 
Nieznane informacje powinny być oznaczone jako nieustalone, a nie zastępowane przypuszczeniami.
 
### BR-009 — Potrzeby i wymagania
 
Schronisko powinno móc opisać:
 
- wymagany poziom aktywności;
- wymagane doświadczenie opiekuna;
- znane reakcje na dzieci;
- znane reakcje na psy;
- znane reakcje na koty;
- potrzebę szczególnej opieki;
- dodatkowe informacje do omówienia przed adopcją.

- Opis stanowi informację przekazaną przez schronisko, a nie gwarancję zachowania zwierzęcia.
 
### BR-010 — Rozróżnianie braku danych
 
System musi odróżniać odpowiedź negatywną od braku informacji.
 
Przykład:
 
> „Nie sprawdzono reakcji na koty” nie oznacza „akceptuje koty” ani „nie akceptuje kotów”.
 
### BR-011 — Zakres danych publicznych
 
Publiczna karta nie może zawierać:
 
- danych poprzednich właścicieli;
- danych kandydatów do adopcji;
- wewnętrznych notatek pracowników;
- pełnej dokumentacji weterynaryjnej.
 
Może zawierać opis potrzeb zdrowotnych i opiekuńczych istotnych dla przyszłego opiekuna.
 
### BR-012 — Statusy zwierzęcia
 
Karta może mieć status:
 
- szkic;
- dostępny do adopcji;
- proces adopcyjny w toku;
- adoptowany;
- wycofany.
 
Powrót ze statusu „proces adopcyjny w toku” do „dostępny do adopcji” powinien być możliwy.
 
Karty adoptowane i wycofane nie pojawiają się w aktywnych wynikach wyszukiwania.
 
---
 
## 8. Wyszukiwanie i przeglądanie
 
### BR-013 — Przeglądanie bez rejestracji
 
Przeglądanie publicznych kart i korzystanie z wyszukiwarki nie wymaga konta.
 
### BR-014 — Wyszukiwanie schronisk
 
Użytkownik powinien móc wyszukiwać schroniska według:
 
- nazwy;
- województwa;
- miejscowości.
 
### BR-015 — Filtrowanie zwierząt
 
Użytkownik powinien móc filtrować zwierzęta według:
 
- gatunku;
- województwa;
- miejscowości;
- schroniska;
- przedziału wieku;
- płci;
- wielkości.
 
### BR-016 — Łączenie filtrów
 
Filtry muszą działać łącznie.
 
Przykład:
 
> Psy, województwo kujawsko-pomorskie, średnia wielkość, wiek od 2 do 6 lat.
 
Dla wieku szacowanego karta spełnia warunek, jeżeli szacowany przedział ma część wspólną z przedziałem wskazanym przez użytkownika.
 
### BR-017 — Dwie ścieżki przeglądania
 
Użytkownik powinien móc:
 
- przeglądać zwierzęta ze wszystkich placówek;
- ograniczyć wyniki do wybranego schroniska.
 
### BR-018 — Informacje na liście wyników
 
Lista powinna pokazywać co najmniej:
 
- zdjęcie;
- imię;
- gatunek;
- wiek lub przedział wieku;
- wielkość;
- lokalizację;
- nazwę placówki;
- status dostępności;
- aktualność danych.
 
### BR-019 — Sortowanie
 
Użytkownik powinien móc sortować wyniki według:
 
- daty publikacji;
- daty potwierdzenia aktualności.
 
### BR-020 — Dostępność w wynikach
 
Domyślnie wyniki obejmują zwierzęta dostępne do adopcji.
 
Użytkownik może dodatkowo wyświetlić zwierzęta ze statusem „proces adopcyjny w toku”, ale nie może wysłać do nich nowego zgłoszenia.
 
---
 
## 9. Ulubione
 
### BR-021 — Zapisywanie zwierząt
 
Zalogowany kandydat powinien móc dodać zwierzę do własnej listy ulubionych i usunąć je z niej.
 
### BR-022 — Prywatna lista
 
Lista ulubionych nie jest publiczna.
 
### BR-023 — Aktualny status
 
Na liście ulubionych powinien być widoczny aktualny status zwierzęcia.
 
Zapisanie do ulubionych nie oznacza rezerwacji ani zgłoszenia zainteresowania adopcją.
 
---
 
## 10. Profil warunków adopcyjnych
 
### BR-024 — Zakres profilu
 
Kandydat powinien móc określić:
 
- obecność dzieci w domu;
- obecność psów;
- obecność kotów;
- doświadczenie w opiece nad zwierzętami;
- czas i możliwości zapewnienia aktywności;
- gotowość do szczególnej opieki.
 
Pytania powinny mieć zdefiniowane warianty odpowiedzi oraz możliwość pozostawienia odpowiedzi nieuzupełnionej.
 
### BR-025 — Edycja profilu
 
Kandydat powinien móc zmieniać zapisane odpowiedzi.
 
Zmiana profilu nie może nadpisywać odpowiedzi już przesłanych ze zgłoszeniem.
 
### BR-026 — Prywatność profilu
 
Profil warunków adopcyjnych nie jest publiczny.
 
Schronisko otrzymuje odpowiedzi wyłącznie w zgłoszeniu skierowanym do jego placówki.
 
---
 
## 11. Dopasowanie z wyjaśnieniem
 
Dopasowanie jest głównym wyróżnikiem projektu i obowiązkową częścią MVP.
 
Jego celem jest przygotowanie kandydata i schroniska do rozmowy, a nie automatyczna kwalifikacja do adopcji.
 
### BR-027 — Porównywanie warunków
 
System powinien porównywać odpowiedzi kandydata z uporządkowanymi wymaganiami zwierzęcia.
 
W MVP porównanie obejmuje:
 
- obecność dzieci;
- obecność psów;
- obecność kotów;
- doświadczenie opiekuna;
- poziom aktywności;
- gotowość do szczególnej opieki.
 
### BR-028 — Kategorie wyniku
 
Dla każdego kryterium system prezentuje jedną z kategorii:
 
- zgodność z opisanym wymaganiem;
- rozbieżność wymagająca rozmowy;
- brak danych do oceny;
- nie dotyczy.
 
### BR-029 — Wyjaśnienie wyniku
 
Każda ocena powinna zawierać przyczynę wynikającą z odpowiedzi kandydata i danych zwierzęcia.
 
Przykład:
 
> Deklarujesz posiadanie kota, ale reakcja tego psa na koty nie została sprawdzona. Tę kwestię należy omówić ze schroniskiem.
 
### BR-030 — Brak pozornej pewności
 
System nie powinien prezentować:
 
- procentowej gwarancji udanej adopcji;
- automatycznej decyzji o przyjęciu lub odrzuceniu kandydata;
- gwarancji zachowania zwierzęcia;
- diagnoz medycznych lub behawioralnych.
 
### BR-031 — Brak danych nie oznacza zgodności
 
Nieuzupełniona odpowiedź lub nieznana cecha zwierzęcia nie może zwiększać oceny dopasowania.
 
### BR-032 — Możliwość zgłoszenia mimo rozbieżności
 
Kandydat może wysłać zgłoszenie mimo rozbieżności po zapoznaniu się z ich podsumowaniem.
 
Niekompletny profil również nie blokuje zgłoszenia. Brakujące odpowiedzi muszą być widoczne dla schroniska.
 
### BR-033 — Powtarzalność
 
Te same odpowiedzi i wymagania ocenione według tej samej wersji reguł powinny dawać ten sam wynik.
 
Mechanizm może działać na zdefiniowanych regułach i nie wymaga AI.
 
### Przykładowe reguły dopasowania
 
| Sytuacja | Wynik |
|---|---|
| Kandydat ma kota, a pies według opisu nie akceptuje kotów | Rozbieżność wymagająca rozmowy |
| Kandydat ma kota, a reakcja psa na koty jest nieznana | Brak danych do oceny |
| Zwierzę wymaga doświadczenia, a kandydat deklaruje jego brak | Rozbieżność wymagająca rozmowy |
| Deklarowana aktywność odpowiada wymaganej | Zgodność w tym kryterium |
| Kandydat nie odpowiedział na pytanie o szczególną opiekę | Brak danych do oceny |
| Kandydat nie ma kota, a sprawdzana jest obecność kota | Nie dotyczy |
 
Znaczenie kategorii oraz treść pytań należy skonsultować z przedstawicielem schroniska przed pilotażem.
 
---
 
## 12. Zgłoszenia zainteresowania adopcją
 
### BR-034 — Wysłanie zgłoszenia
 
Zalogowany kandydat może wysłać zgłoszenie dotyczące konkretnego zwierzęcia dostępnego do adopcji.
 
Zgłoszenie zawiera:
 
- dane kontaktowe;
- wiadomość do schroniska;
- odpowiedzi z profilu warunków;
- wynik dopasowania z wyjaśnieniem, jeżeli został wykonany;
- datę wysłania.
 
Przed wysłaniem użytkownik widzi, jakie dane zostaną przekazane.
 
### BR-035 — Znaczenie zgłoszenia
 
Zgłoszenie nie jest rezerwacją, umową ani gwarancją adopcji.
 
System powinien wyraźnie informować o tym użytkownika.
 
### BR-036 — Statusy zgłoszenia
 
Zgłoszenie może mieć status:
 
- nowe;
- w kontakcie;
- zakończone adopcją;
- zakończone bez adopcji;
- wycofane przez kandydata.
 
### BR-037 — Obsługa zgłoszenia
 
Pracownik właściwego schroniska może:
 
- przeglądać zgłoszenie;
- zmieniać jego status;
- przekazywać kandydatowi informację o dalszych krokach.
 
Rozbudowany czat nie jest wymagany w MVP.
 
### BR-038 — Historia statusów
 
Każda zmiana statusu powinna zawierać:
 
- poprzedni i nowy status;
- datę zmiany;
- autora zmiany;
- opcjonalną wiadomość dla kandydata.
 
### BR-039 — Ograniczenie duplikatów
 
Kandydat nie może mieć więcej niż jednego niezakończonego zgłoszenia do tego samego zwierzęcia.
 
Może zgłaszać zainteresowanie różnymi zwierzętami.
 
### BR-040 — Wycofanie zgłoszenia
 
Kandydat może wycofać własne niezakończone zgłoszenie.
 
Wycofanie nie usuwa historii jego obsługi.
 
### BR-041 — Zachowanie stanu z chwili wysłania
 
Zgłoszenie zachowuje odpowiedzi kandydata, wymagania zwierzęcia i wynik dopasowania z chwili wysłania.
 
Późniejsze zmiany danych nie mogą nadpisywać tej historii.
 
### BR-042 — Zakończenie adopcji
 
Zakończenie zgłoszenia adopcją powinno:
 
- ustawić status zwierzęcia na „adoptowany”;
- usunąć kartę z aktywnych wyników;
- zamknąć pozostałe niezakończone zgłoszenia do tego zwierzęcia;
- poinformować pozostałych kandydatów o zakończeniu ogłoszenia.
 
Pracownik powinien móc również oznaczyć adopcję przeprowadzoną poza portalem.
 
### BR-043 — Powiadomienia
 
System powinien wysyłać powiadomienia e-mail:
 
- do kandydata po wysłaniu zgłoszenia;
- do schroniska po otrzymaniu zgłoszenia;
- do kandydata po zmianie statusu.
 
E-mail nie powinien zawierać pełnej ankiety. Szczegóły są dostępne po zalogowaniu.
 
---
 
## 13. Aktualność i jakość danych
 
### BR-044 — Potwierdzenie aktualności
 
Pracownik może potwierdzić, że karta i status zwierzęcia są aktualne.
 
System zapisuje datę i osobę potwierdzającą.
 
Sama zmiana tekstu opisu nie zastępuje potwierdzenia aktualności.
 
### BR-045 — Oznaczenie niepotwierdzonych kart
 
Proponowany próg MVP wynosi 30 dni od ostatniego potwierdzenia.
 
Po jego przekroczeniu karta otrzymuje oznaczenie:
 
> Dostępność wymaga potwierdzenia.
 
Nie powoduje to automatycznego usunięcia karty ani oznaczenia zwierzęcia jako adoptowanego.
 
Wartość 30 dni jest założeniem do zatwierdzenia.
 
### BR-046 — Przypomnienia dla schroniska
 
Schronisko powinno otrzymywać zbiorcze przypomnienie o kartach wymagających potwierdzenia, nie częściej niż raz w tygodniu.
 
### BR-047 — Źródło danych
 
W MVP dane i zdjęcia dodają uprawnieni pracownicy lub administrator działający za zgodą placówki.
 
Projekt nie zakłada automatycznego dostępu do danych wszystkich schronisk w Polsce.
 
Dane demonstracyjne muszą być fikcyjne lub udostępnione za zgodą uprawnionych podmiotów.
 
---
 
## 14. Administracja i prywatność
 
### BR-048 — Moderacja
 
Administrator może ukryć ogłoszenie lub zablokować konto z podaniem powodu.
 
Moderacja nie może bez wyjaśnienia usuwać historii zgłoszeń.
 
### BR-049 — Ograniczenie dostępu
 
Kandydat widzi wyłącznie własne zgłoszenia.
 
Pracownik widzi wyłącznie zgłoszenia dotyczące jego schroniska.
 
Zmiana identyfikatora w adresie strony nie może pozwalać na odczyt cudzych danych.
 
### BR-050 — Minimalizacja danych
 
MVP nie wymaga:
 
- numeru PESEL;
- skanu dokumentu tożsamości;
- dokładnego adresu zamieszkania;
- danych identyfikujących dzieci i innych domowników.
 
Dane kontaktowe obejmują imię, e-mail i opcjonalnie telefon.
 
### BR-051 — Zasady przechowywania danych
 
Przed uruchomieniem operacyjnym należy ustalić:
 
- odpowiedzialność za dane;
- okresy przechowywania;
- zasady usuwania lub anonimizacji;
- sposób obsługi żądań użytkowników;
- zakres informacji przekazywanych użytkownikom.
 
Zachowanie historii biznesowej nie oznacza bezterminowego przechowywania danych osobowych.

---
 
## 15. Reguły biznesowe
 
### RB-001
 
Tylko zatwierdzona i niezablokowana placówka może publikować karty zwierząt.
 
### RB-002
 
W MVP zwierzę jest przypisane do jednej placówki.
 
### RB-003
 
Nowe zgłoszenia można wysyłać wyłącznie do zwierząt dostępnych do adopcji.
 
### RB-004
 
Brak danych, odpowiedź negatywna i „nie dotyczy” są odrębnymi stanami.
 
### RB-005
 
Dopasowanie nie zatwierdza ani nie odrzuca kandydata.
 
### RB-006
 
Rozbieżność nie blokuje wysłania zgłoszenia.
 
### RB-007
 
Zmiana profilu kandydata nie nadpisuje wcześniej wysłanych odpowiedzi.
 
### RB-008
 
Kandydat może mieć najwyżej jedno niezakończone zgłoszenie do danego zwierzęcia.
 
### RB-009
 
Kolejność zgłoszeń nie daje prawa do adopcji.
 
### RB-010
 
Zapis do ulubionych nie jest zgłoszeniem ani rezerwacją.
 
### RB-011
 
Adopcja kończy aktywną publikację i zamyka pozostałe niezakończone zgłoszenia do zwierzęcia.
 
### RB-012
 
Brak potwierdzenia aktualności nie oznacza, że zwierzę zostało adoptowane.
 
---
 
## 16. Przykładowe scenariusze biznesowe
 
### UC-001 — Znalezienie zwierzęcia
 
Gość wybiera gatunek, województwo i wielkość.
 
System prezentuje pasujące zwierzęta dostępne do adopcji.
 
Po otwarciu karty użytkownik widzi potrzeby, lokalizację, zasady adopcji i aktualność informacji.
 
### UC-002 — Przeglądanie schroniska
 
Użytkownik znajduje schronisko według miejscowości.
 
Otwiera profil placówki i przegląda jej podopiecznych.
 
### UC-003 — Dopasowanie przy brakujących danych
 
Kandydat deklaruje posiadanie kota.
 
Reakcja wybranego psa na koty jest nieznana.
 
System wskazuje brak danych i konieczność rozmowy, zamiast potwierdzać zgodność.
 
### UC-004 — Zgłoszenie mimo rozbieżności
 
Kandydat zapoznaje się z wyjaśnieniem i wysyła zgłoszenie.
 
Schronisko otrzymuje odpowiedzi, wynik porównania i wiadomość kandydata.
 
### UC-005 — Obsługa zgłoszenia
 
Pracownik otwiera zgłoszenie dotyczące swojej placówki.
 
Zmienia status na „w kontakcie” i przekazuje informację o dalszych krokach.
 
Kandydat widzi zmianę i otrzymuje powiadomienie.
 
### UC-006 — Zakończenie adopcji
 
Pracownik oznacza zgłoszenie jako zakończone adopcją.
 
Zwierzę znika z aktywnych wyników, a pozostali zainteresowani otrzymują informację o zakończeniu ogłoszenia.
 
### UC-007 — Potwierdzenie aktualności
 
Karta przekracza ustalony termin potwierdzenia.
 
System oznacza ją ostrzeżeniem.
 
Pracownik sprawdza dane i potwierdza aktualność, usuwając ostrzeżenie.
 
---
 
## 17. Zakres MVP
 
Obowiązkowy zakres pierwszej wersji:
 
1. konta użytkowników i role;
2. zgłaszanie i zatwierdzanie schronisk;
3. profile placówek;
4. karty psów i kotów;
5. publikacja i zmiana statusów;
6. katalog, filtrowanie i sortowanie;
7. ulubione;
8. profil warunków adopcyjnych;
9. dopasowanie z wyjaśnieniem;
10. zgłoszenia zainteresowania;
11. obsługa i historia statusów;
12. potwierdzanie aktualności;
13. podstawowe powiadomienia e-mail;
14. moderacja i ograniczenia dostępu.
 
Produkt powinien działać jako responsywna aplikacja webowa.
 
Proponowany zakres demonstracyjny:
 
- 3–5 placówek;
- 30–50 kart zwierząt;
- konta demonstracyjne dla wszystkich ról;
- przykładowe zgłoszenia w różnych statusach.
 
Liczby te stanowią założenie do demonstracji, nie zobowiązanie do pozyskania rzeczywistych placówek.
 
---
 
## 18. Poza zakresem MVP
 
Poza pierwszą wersją pozostają:
 
- objęcie wszystkich schronisk w Polsce;
- automatyczne pobieranie danych z innych stron;
- synchronizacja z zewnętrznymi systemami;
- mapa i filtrowanie według promienia odległości;
- natywna aplikacja mobilna;
- praca offline;
- pełna dokumentacja weterynaryjna;
- zarządzanie leczeniem, dyżurami i wolontariatem;
- magazyn leków i karmy;
- płatności i zbiórki;
- generowanie i podpisywanie umów adopcyjnych;
- rozbudowany czat;
- rezerwowanie wizyt;
- automatyczne diagnozy;
- procentowe gwarancje dopasowania;
- automatyczna kwalifikacja kandydatów;
- transfery kart między placówkami.
 
---
 
## 19. Kryteria akceptacji MVP
 
### AC-001 — Wyszukiwanie
 
Można znaleźć zwierzęta, łącząc filtry gatunku, województwa, wieku i wielkości.
 
### AC-002 — Profil schroniska
 
Profil placówki pokazuje jej dane i opublikowane karty zgodnie z wybranym statusem.
 
### AC-003 — Karta zwierzęcia
 
Karta prezentuje dane podstawowe, zdjęcie, potrzeby, placówkę, status i aktualność.
 
### AC-004 — Zatwierdzenie placówki
 
Niezatwierdzone schronisko nie może opublikować karty.
 
### AC-005 — Uprawnienia pracowników
 
Pracownik nie może odczytać ani zmienić niepublicznych danych innej placówki.
 
### AC-006 — Ulubione
 
Kandydat może dodać i usunąć zwierzę z ulubionych bez tworzenia zgłoszenia.
 
### AC-007 — Kategorie dopasowania
 
System rozróżnia zgodność, rozbieżność, brak danych i „nie dotyczy”.
 
### AC-008 — Brak danych
 
Przy nieznanej reakcji psa na koty i obecności kota u kandydata system nie przedstawia zgodności.
 
### AC-009 — Wyjaśnienie
 
Wynik zawiera przyczyny, ale nie prezentuje gwarancji ani automatycznej decyzji o adopcji.
 
### AC-010 — Zgłoszenie mimo rozbieżności
 
Kandydat może wysłać zgłoszenie po zapoznaniu się z rozbieżnościami.
 
### AC-011 — Duplikaty zgłoszeń
 
System blokuje drugie niezakończone zgłoszenie tej samej osoby do tego samego zwierzęcia.
 
### AC-012 — Zachowanie odpowiedzi
 
Zmiana profilu kandydata nie modyfikuje odpowiedzi w już wysłanym zgłoszeniu.
 
### AC-013 — Prywatność zgłoszeń
 
Kandydat widzi własne zgłoszenia, ale nie zgłoszenia innych osób.
 
### AC-014 — Historia statusów
 
Zmiana statusu zapisuje autora i datę oraz inicjuje powiadomienie.
 
### AC-015 — Adopcja
 
Oznaczenie adopcji usuwa zwierzę z aktywnych wyników i zamyka pozostałe niezakończone zgłoszenia.
 
### AC-016 — Nieaktualna karta
 
Po przekroczeniu progu aktualności pojawia się ostrzeżenie bez automatycznej zmiany statusu adopcji.
 
### AC-017 — Potwierdzenie aktualności
 
Potwierdzenie usuwa ostrzeżenie i zapisuje datę oraz osobę potwierdzającą.
 
### AC-018 — Wycofanie zgłoszenia
 
Kandydat może wycofać własne niezakończone zgłoszenie.
 
### AC-019 — Brak ujawnienia danych
 
Publiczne widoki i powiadomienia e-mail nie ujawniają ankiet ani danych innych kandydatów.
 
### AC-020 — Obsługa na telefonie
 
Wyszukiwanie, karta zwierzęcia, profil warunków i wysłanie zgłoszenia są dostępne na urządzeniu mobilnym.
 
---
 
## 20. Kluczowe pytania otwarte
 
Do doprecyzowania przed realizacją:
 
1. Które schronisko skonsultuje pytania i reguły dopasowania?
2. Jak administrator potwierdza uprawnienie przedstawiciela placówki?
3. Czy w kolejnych wersjach obsługujemy także fundacje i domy tymczasowe?
4. Jak definiujemy kategorie wielkości i poziomy aktywności?
5. Jak definiujemy poziomy doświadczenia kandydata?
6. Czy próg 30 dni na potwierdzenie aktualności odpowiada potrzebom placówek?
7. Jakie dane kontaktowe kandydata są niezbędne?
8. Kto odpowiada za dane i jakie okresy przechowywania przyjmujemy?
9. Jak obsłużyć usunięcie konta z niezakończonym zgłoszeniem?
10. Czy placówki akceptują blokadę nowych zgłoszeń przy statusie „proces adopcyjny w toku”?
11. Jakie materiały można wykorzystać w wersji demonstracyjnej?
12. Czy po zakończonym zgłoszeniu kandydat może od razu wysłać kolejne do tego samego zwierzęcia?
 
---
 
## 21. Definicja sukcesu projektu
 
Projekt osiąga podstawowy cel, jeżeli kandydat może:
 
1. znaleźć zwierzę odpowiadające podstawowym kryteriom;
2. poznać jego potrzeby i zasady adopcji;
3. zrozumieć zgodności, rozbieżności i brakujące informacje dotyczące swoich warunków;
4. przesłać zgłoszenie do właściwego schroniska;
5. sprawdzić dalszy status zgłoszenia.
 
Pracownik schroniska powinien móc:
 
1. opublikować i aktualizować kartę;
2. obsłużyć zgłoszenie;
3. zmienić status;
4. zakończyć ogłoszenie po adopcji;
5. zachować historię obsługi zgodnie z przyjętymi zasadami przechowywania danych.
