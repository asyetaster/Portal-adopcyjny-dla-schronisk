# PORTAL ADOPCYJNY DLA SCHRONISK
## Wymagania biznesowe - wersja animal-centered

Wersja 0.1
Status: Draft
Główny cel: wyszukiwanie zwierząt do adopcji i wspieranie kontaktu ze schroniskami
Źródło danych: profile i karty zwierząt publikowane przez schroniska
Zakres geograficzny: Polska, z pilotażem na ograniczonej liczbie placówek

---

## 1. Cel projektu

Celem projektu jest stworzenie portalu łączącego schroniska z osobami, które chcą adoptować zwierzę lub pomóc w inny sposób.

Platforma ma umożliwiać:

- wyszukiwanie schronisk i zwierząt dostępnych do adopcji;
- poznanie potrzeb i charakteru zwierzęcia;
- porównanie potrzeb zwierzęcia z warunkami deklarowanymi przez potencjalnego opiekuna;
- przesłanie zgłoszenia zainteresowania adopcją;
- obsługę zgłoszeń przez pracowników schroniska;
- utrzymywanie aktualnych informacji o dostępności zwierząt;
- finansowe wsparcie schroniska lub wskazanego zwierzęcia;
- przeglądanie historii i statystyk wsparcia;
- zgłoszenie chęci udziału w wolontariacie;
- zgłoszenie się do wyprowadzania psów na spacery;
- zarządzanie zgłoszeniami do pomocy przez schronisko.

Przykładowe pytania biznesowe:

> Znajdź psy średniej wielkości, w wieku do 5 lat, w moim województwie, które według informacji schroniska mogą mieszkać z dziećmi.

> Nie mogę adoptować psa, ale chcę wesprzeć jego schronisko kwotą 30 zł, wskazując go jako cel wsparcia.

> Chcę pomagać w schronisku albo zapisać się na spacer z psem w dostępnym terminie.

Portal wspiera proces adopcyjny, ale nie podejmuje decyzji o adopcji.

Wpłata nie daje pierwszeństwa w adopcji ani uprawnienia do kontaktu ze zwierzęciem.

Zgłoszenie do wolontariatu lub na spacer wymaga akceptacji schroniska zgodnie z jego zasadami.

---

## 2. Główna zasada produktu

Centralnym obiektem platformy pozostaje zwierzę i jego potrzeby.

Schronisko jest źródłem informacji o zwierzęciu oraz podmiotem odpowiedzialnym za obsługę adopcji i organizowanie pomocy.

Oznacza to, że:

- zwierzę jest głównym obiektem wyszukiwania;
- schronisko, lokalizacja i zasady adopcji stanowią kontekst jego karty;
- użytkownik powinien móc szybko przejść od listy zwierząt do pełnej karty;
- dopasowanie warunków przygotowuje rozmowę ze schroniskiem, ale nie zastępuje jego decyzji;
- aktualność ogłoszenia powinna być widoczna;
- adopcja nie jest jedynym sposobem pomocy;
- wsparcie finansowe, wolontariat i spacery są niezależne od profilu adopcyjnego;
- możliwość spaceru ze zwierzęciem jest określana przez schronisko, a nie automatycznie na podstawie statusu adopcyjnego.

---

## 3. Główne zastosowania biznesowe

Platforma ma wspierać:

1. wyszukiwanie zwierząt według lokalizacji i podstawowych cech;
2. przeglądanie schronisk i ich podopiecznych;
3. poznawanie potrzeb, charakteru i wymagań zwierzęcia;
4. zapisywanie interesujących zwierząt do ulubionych;
5. określanie warunków, jakie kandydat może zapewnić;
6. otrzymywanie wyjaśnienia zgodności i rozbieżności między warunkami kandydata a potrzebami zwierzęcia;
7. przesyłanie zgłoszeń zainteresowania adopcją;
8. obsługę zgłoszeń przez schroniska;
9. aktualizowanie dostępności zwierząt;
10. ograniczanie liczby nieaktualnych ogłoszeń;
11. jednorazowe wsparcie finansowe wybranego schroniska;
12. wsparcie schroniska ze wskazaniem konkretnego zwierzęcia;
13. przeglądanie historii wpłat przez użytkownika i schronisko;
14. prezentowanie zbiorczych statystyk wsparcia;
15. zgłaszanie chęci udziału w wolontariacie;
16. publikowanie terminów spacerów i przyjmowanie zgłoszeń;
17. zarządzanie zgłoszeniami do pomocy przez schronisko.

---

## 4. Użytkownicy i role

### 4.1. Gość

Użytkownik niezalogowany może:

- przeglądać katalog schronisk;
- wyszukiwać zwierzęta i korzystać z filtrów;
- przeglądać publiczne karty;
- zapoznawać się z zasadami adopcji;
- przeglądać publiczne statystyki wsparcia;
- sprawdzać zasady wolontariatu i dostępne terminy spacerów.

W MVP wykonanie wpłaty oraz wysłanie zgłoszenia wymaga zalogowania.

### 4.2. Użytkownik zarejestrowany

Użytkownik może pełnić jednocześnie funkcję kandydata do adopcji, darczyńcy i osoby zainteresowanej wolontariatem.

Może:

- zarządzać własnym profilem;
- zapisać warunki adopcyjne;
- korzystać z dopasowania z wyjaśnieniem;
- dodawać zwierzęta do ulubionych;
- wysyłać zgłoszenia adopcyjne;
- sprawdzać status własnych zgłoszeń i nimi zarządzać;
- wspierać finansowo schroniska i wskazane zwierzęta;
- przeglądać własną historię wpłat;
- zgłaszać się do wolontariatu;
- zgłaszać się na spacery;
- sprawdzać status i wycofywać własne zgłoszenia do pomocy.

Uzupełnienie profilu adopcyjnego nie jest wymagane do wpłat, wolontariatu ani spacerów.

### 4.3. Pracownik schroniska

Użytkownik przypisany do placówki może:

- zarządzać profilem swojego schroniska;
- tworzyć i aktualizować karty zwierząt;
- określać potrzeby i wymagania zwierząt;
- zmieniać statusy dostępności;
- potwierdzać aktualność ogłoszeń;
- przeglądać i obsługiwać zgłoszenia adopcyjne;
- przeglądać wpłaty dotyczące swojej placówki;
- przeglądać wpłaty ze wskazaniem konkretnych zwierząt;
- zarządzać informacjami o wolontariacie;
- obsługiwać zgłoszenia wolontariackie;
- publikować i anulować terminy spacerów;
- akceptować, odrzucać i obsługiwać zgłoszenia na spacery.

Pracownik nie może dowolnie oznaczyć nieopłaconej transakcji jako opłaconej.

### 4.4. Administrator

Administrator odpowiada za:

- zatwierdzanie kont schronisk;
- moderowanie ogłoszeń;
- blokowanie kont i placówek w przypadku nadużyć;
- nadzór nad aktywacją funkcji przyjmowania wpłat;
- dostęp do informacji potrzebnych do wyjaśniania problemów i nadużyć.

Zatwierdzenie profilu schroniska nie oznacza automatycznego uruchomienia płatności.

---

## 5. Główne obiekty biznesowe

Platforma powinna operować na następujących obiektach:

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
- potwierdzenie aktualności ogłoszenia;
- wpłata;
- odbiorca środków przypisany do schroniska;
- cel wpłaty: schronisko albo wskazane zwierzę;
- status płatności i ewentualny zwrot;
- statystyki wsparcia;
- zgłoszenie do wolontariatu;
- termin spaceru;
- zgłoszenie na spacer;
- historia obsługi zgłoszeń do pomocy.

W MVP obsługiwane gatunki to psy i koty.

Moduł spacerów dotyczy psów wskazanych przez schronisko jako dostępne do tej formy pomocy.

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

Profil może dodatkowo prezentować:

- możliwość wsparcia finansowego;
- publiczne statystyki wsparcia;
- zasady i dostępność wolontariatu;
- dostępne terminy spacerów.

### BR-003 — Rejestracja placówki

Przedstawiciel schroniska powinien móc zgłosić placówkę do zatwierdzenia przez administratora.

### BR-004 — Weryfikacja przed publikacją

Niezatwierdzona placówka może przygotowywać dane, ale nie może publikować publicznych kart zwierząt ani ofert pomocy.

Administrator ręcznie weryfikuje uprawnienie przedstawiciela do prowadzenia profilu.

Zatwierdzenie profilu nie oznacza certyfikacji warunków opieki w placówce.

### BR-005 — Zarządzanie własną placówką

Pracownik może zarządzać wyłącznie placówką, do której został przypisany.

Dotyczy to również wpłat, wolontariatu i spacerów.

---

## 7. Karta zwierzęcia

### BR-006 — Jednoznaczna karta

Każde zwierzę powinno posiadać stały identyfikator i być przypisane do jednego schroniska.

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

Karta może dodatkowo zawierać przycisk wsparcia, statystyki wpłat oraz dostępne terminy spacerów.

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

Opis stanowi informację przekazaną przez schronisko, a nie gwarancję zachowania zwierzęcia.

### BR-010 — Rozróżnianie braku danych

System musi odróżniać odpowiedź negatywną od braku informacji.

Przykład:

> „Nie sprawdzono reakcji na koty” nie oznacza „akceptuje koty” ani „nie akceptuje kotów”.

### BR-011 — Zakres danych publicznych

Publiczna karta nie może zawierać:

- danych poprzednich właścicieli;
- danych kandydatów do adopcji;
- danych osób zgłaszających się do pomocy;
- danych identyfikujących darczyńców;
- wewnętrznych notatek pracowników;
- pełnej dokumentacji weterynaryjnej.

Może zawierać opis potrzeb zdrowotnych i opiekuńczych oraz zbiorcze statystyki wsparcia.

### BR-012 — Statusy zwierzęcia

Karta może mieć status:

- szkic;
- dostępny do adopcji;
- proces adopcyjny w toku;
- adoptowany;
- wycofany.

Powrót ze statusu „proces adopcyjny w toku” do „dostępny do adopcji” powinien być możliwy.

Karty adoptowane i wycofane nie pojawiają się w aktywnych wynikach wyszukiwania.

Dostępność wsparcia finansowego i spacerów jest określana osobno. Status adopcyjny nie daje automatycznie możliwości spaceru.

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

Użytkownik może dodatkowo wyświetlić zwierzęta ze statusem „proces adopcyjny w toku”, ale nie może wysłać do nich nowego zgłoszenia adopcyjnego.

Ograniczenie to nie wyklucza innych form pomocy, jeśli schronisko je udostępniło.

---

## 9. Ulubione

### BR-021 — Zapisywanie zwierząt

Zalogowany użytkownik powinien móc dodać zwierzę do własnej listy ulubionych i usunąć je z niej.

### BR-022 — Prywatna lista

Lista ulubionych nie jest publiczna.

### BR-023 — Aktualny status

Na liście ulubionych powinien być widoczny aktualny status zwierzęcia.

Zapisanie do ulubionych nie oznacza rezerwacji, wpłaty ani zgłoszenia zainteresowania adopcją lub spacerem.

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

Schronisko otrzymuje odpowiedzi wyłącznie w zgłoszeniu adopcyjnym skierowanym do jego placówki.

Zgłoszenie do wolontariatu, na spacer lub dokonanie wpłaty nie udostępnia automatycznie profilu adopcyjnego.

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
- zamknąć pozostałe niezakończone zgłoszenia adopcyjne;
- poinformować pozostałych kandydatów o zakończeniu ogłoszenia.

Pracownik powinien móc również oznaczyć adopcję przeprowadzoną poza portalem.

Wpłaty zachowują historię. Przyszłe spacery podlegają zasadom opisanym w module spacerów.

### BR-043 — Powiadomienia adopcyjne

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

Moderacja nie może bez wyjaśnienia usuwać historii zgłoszeń ani wpłat.

Blokada placówki wyłącza nowe wpłaty, nowe zgłoszenia do pomocy i publikację nowych terminów. Istniejące sprawy wymagają obsługi lub przekazania informacji zainteresowanym.

### BR-049 — Ograniczenie dostępu

Użytkownik widzi wyłącznie własne zgłoszenia i historię wpłat.

Pracownik widzi dane dotyczące jego schroniska.

Zmiana identyfikatora w adresie strony nie może pozwalać na odczyt cudzych danych.

Dane dostępne w module wpłat nie obejmują pełnych danych instrumentu płatniczego.

### BR-050 — Minimalizacja danych

MVP nie wymaga:

- numeru PESEL;
- skanu dokumentu tożsamości;
- dokładnego adresu zamieszkania;
- danych identyfikujących dzieci i innych domowników.

Dane kontaktowe obejmują imię, e-mail i opcjonalnie telefon.

Formularz wolontariatu może zawierać oświadczenie o spełnieniu wymagań wieku, bez obowiązkowego zbierania pełnej daty urodzenia.

Portal nie przechowuje numerów kart płatniczych ani kodów zabezpieczających.

### BR-051 — Zasady przechowywania danych

Przed uruchomieniem operacyjnym należy ustalić:

- odpowiedzialność za dane;
- okresy przechowywania;
- zasady usuwania lub anonimizacji;
- sposób obsługi żądań użytkowników;
- zakres informacji przekazywanych użytkownikom;
- zasady przechowywania danych płatniczych i rozliczeniowych;
- zasady przechowywania zgłoszeń do wolontariatu i spacerów.

Zachowanie historii biznesowej nie oznacza bezterminowego przechowywania wszystkich danych osobowych.

Usunięcie konta nie może być traktowane jako automatyczny zwrot wpłat ani powód do utraty wymaganych zapisów rozliczeniowych.

---

## 15. Wsparcie finansowe — „Nakarm psiaka”

### BR-052 — Wybór celu wsparcia

Zalogowany użytkownik może rozpocząć wsparcie:

- z profilu schroniska — jako wsparcie całej placówki;
- z karty zwierzęcia — jako wsparcie placówki ze wskazaniem tego zwierzęcia.

Na karcie psa przycisk może mieć nazwę „Nakarm psiaka”. Na profilu schroniska i kartach innych zwierząt należy użyć odpowiedniego komunikatu, np. „Wesprzyj schronisko” lub „Wesprzyj opiekę”.

Jest to rzeczywista płatność użytkownika, a nie bezpłatne kliknięcie finansowane przez portal lub sponsora.

### BR-053 — Wybór kwoty

Użytkownik może wybrać sugerowaną kwotę albo wpisać własną.

MVP obsługuje:

- wpłaty jednorazowe;
- walutę PLN;
- dodatnie kwoty mieszczące się w limitach skonfigurowanych dla płatności.

Minimalna i maksymalna kwota wymagają uzgodnienia z wybranym operatorem.

Przed zatwierdzeniem użytkownik widzi kwotę, cel oraz odbiorcę wpłaty.

### BR-054 — Odbiorca i przeznaczenie środków

Odbiorcą środków jest zweryfikowany podmiot prowadzący schronisko albo uprawniony do przyjmowania wsparcia na jego rzecz.

Zwierzę jest wskazanym celem wsparcia, a nie osobnym odbiorcą płatności.

Przed wpłatą należy jasno wskazać:

- kto otrzyma środki;
- czy wsparcie dotyczy całej placówki, czy opieki nad wskazanym zwierzęciem;
- na jakie potrzeby może zostać przeznaczone;
- jak postępuje się, gdy potrzeba przestanie być aktualna;
- czy występują opłaty wpływające na kwotę otrzymaną przez odbiorcę.

Samo hasło „Nakarm psiaka” nie może sugerować zakupu konkretnej porcji karmy, jeśli wpłata finansuje szerzej rozumianą opiekę.

Portal nie potwierdza automatycznie, na co środki zostały faktycznie wydane.

### BR-055 — Aktywacja wpłat dla placówki

Przyjmowanie wpłat wymaga:

- zatwierdzonej i niezablokowanej placówki;
- skonfigurowanego odbiorcy środków;
- ukończenia wymaganej konfiguracji i weryfikacji u operatora;
- opublikowania zasad wsparcia.

Nie wystarczy samo wpisanie numeru rachunku w opisie schroniska.

W MVP integracja obejmuje jednego operatora płatności, którego wybór pozostaje otwarty.

### BR-056 — Obsługa i status płatności

Płatność jest realizowana przez zewnętrznego operatora.

Portal rozróżnia co najmniej:

- płatność rozpoczętą lub oczekującą;
- wpłatę potwierdzoną;
- płatność nieudaną;
- płatność anulowaną lub wygasłą;
- wpłatę częściowo zwróconą;
- wpłatę całkowicie zwróconą.

Powrót użytkownika ze strony operatora nie jest samodzielnym dowodem opłacenia.

Status finansowy musi wynikać ze zweryfikowanej informacji operatora. Ponowne przekazanie tej samej informacji nie może utworzyć drugiej wpłaty ani podwoić statystyk.

### BR-057 — Historia wpłat użytkownika

Użytkownik widzi własne wpłaty wraz z:

- datą;
- kwotą i walutą;
- odbiorcą;
- celem wsparcia;
- statusem;
- informacją o ewentualnym zwrocie.

Potwierdzenie wpłaty nie jest automatycznie fakturą ani zaświadczeniem podatkowym.

### BR-058 — Panel wpłat schroniska

Pracownik widzi wpłaty dotyczące swojej placówki, w tym:

- datę;
- kwotę;
- status;
- cel wpłaty;
- wskazane zwierzę, jeżeli dotyczy;
- identyfikator wpłaty;
- kwotę ewentualnego zwrotu.

Lista może być filtrowana według okresu, statusu i zwierzęcia.

Dane identyfikujące darczyńcę są dostępne tylko w zakresie uzasadnionym obsługą i rozliczeniem wsparcia. Panel nie pokazuje pełnych danych instrumentu płatniczego.

### BR-059 — Publiczne statystyki wsparcia

Jeżeli schronisko włączy ich prezentację, profil placówki i karta zwierzęcia mogą pokazywać:

- łączną kwotę wsparcia;
- liczbę skutecznych wpłat;
- liczbę wspierających użytkowników.

Zasady liczenia:

- uwzględnia się tylko potwierdzone wpłaty;
- kwota jest pomniejszana o zwrócone środki, ale nie o prowizje operatora;
- wpłata całkowicie zwrócona nie zwiększa liczby skutecznych wpłat;
- użytkownik z co najmniej jedną niecałkowicie zwróconą wpłatą liczony jest raz w danym zakresie;
- kilka wpłat tej samej osoby nie oznacza kilku wspierających;
- statystyka placówki obejmuje wsparcie ogólne i wsparcie zwierząt bez podwójnego sumowania;
- statystyka zwierzęcia obejmuje wyłącznie wpłaty wskazujące to zwierzę.

Publicznie nie są pokazywane nazwiska, adresy e-mail ani lista transakcji poszczególnych darczyńców.

### BR-060 — Zmiana dostępności zwierzęcia

Nowe wpłaty ze wskazaniem zwierzęcia są możliwe wyłącznie dla opublikowanej karty z aktywną opcją wsparcia.

Adopcja, wycofanie lub ukrycie karty wyłącza rozpoczynanie nowych wpłat na to zwierzę.

Historia dotychczasowych wpłat pozostaje zachowana.

Wpłata rozpoczęta wcześniej zachowuje pierwotny cel. Jeżeli zostanie potwierdzona po zmianie statusu zwierzęcia, sposób jej obsługi wynika z zasad przedstawionych przed płatnością. System nie zmienia celu po cichu.

### BR-061 — Zwroty i problemy z płatnością

Użytkownik powinien mieć informację, z kim skontaktować się w sprawie wpłaty lub zwrotu.

Zwroty w MVP mogą być obsługiwane w panelu operatora, bez rozbudowanego modułu inicjowania zwrotów w portalu.

Portal aktualizuje status i statystyki na podstawie potwierdzonych informacji o zwrocie.

Nieudana płatność nie może być przedstawiana jako udzielone wsparcie.

---

## 16. Zgłoszenia do wolontariatu

### BR-062 — Oferta wolontariatu

Schronisko może włączyć przyjmowanie zgłoszeń oraz opublikować:

- opis możliwych form pomocy;
- wymagania wobec kandydatów;
- informacje o wdrożeniu lub szkoleniu;
- zasady dotyczące wieku;
- dane kontaktowe i dalsze kroki.

Schronisko może czasowo zamknąć nabór bez usuwania wcześniejszych zgłoszeń.

### BR-063 — Formularz zgłoszenia

Zalogowany użytkownik może zgłosić chęć pomocy, podając:

- dane kontaktowe;
- preferowane formy pomocy;
- orientacyjną dostępność;
- doświadczenie;
- wiadomość dla schroniska;
- wymagane oświadczenia dotyczące zapoznania się z zasadami.

Formularz nie wymaga profilu adopcyjnego.

Przed wysłaniem użytkownik widzi przekazywane dane i wymagania placówki.

### BR-064 — Obsługa i statusy zgłoszenia

Zgłoszenie może mieć status:

- nowe;
- w kontakcie;
- zaakceptowane;
- odrzucone;
- wycofane przez użytkownika.

Pracownik może zmienić status i przekazać użytkownikowi informację o dalszych krokach.

Każda zmiana zapisuje autora i datę.

Akceptacja w portalu oznacza pozytywną obsługę zgłoszenia. Nie zastępuje wymaganych przez placówkę formalności, wdrożenia ani szkolenia.

### BR-065 — Duplikaty i wycofanie

Użytkownik może mieć najwyżej jedno aktywne zgłoszenie wolontariackie do danej placówki.

Za aktywne uznaje się zgłoszenie nowe, w kontakcie lub zaakceptowane.

Użytkownik może wycofać aktywne zgłoszenie. Historia pozostaje dostępna zgodnie z zasadami przechowywania danych.

Po odrzuceniu lub wycofaniu może wysłać nowe zgłoszenie.

### BR-066 — Widoczność i powiadomienia

Użytkownik widzi własne zgłoszenia wolontariackie i ich statusy.

Pracownik widzi zgłoszenia skierowane do jego placówki.

System informuje e-mailem:

- schronisko o nowym zgłoszeniu;
- użytkownika o przyjęciu zgłoszenia;
- użytkownika o zmianie statusu.

Lista wolontariuszy i ich dostępność nie są publiczne.

---

## 17. Zgłoszenia na spacery z psami

### BR-067 — Udostępnianie spacerów

Schronisko decyduje, które psy mogą uczestniczyć w spacerach i jakie warunki muszą spełnić osoby zgłaszające się.

Może wymagać np.:

- wcześniejszego kontaktu;
- zaakceptowanego zgłoszenia wolontariackiego;
- odbycia wdrożenia;
- potwierdzenia dodatkowych warunków przed akceptacją.

Akceptacja zgłoszenia wolontariackiego nie daje automatycznego dostępu do każdego psa.

### BR-068 — Publikowanie terminu

Pracownik może opublikować termin spaceru zawierający:

- schronisko;
- wskazanego psa;
- datę;
- godzinę rozpoczęcia i zakończenia;
- miejsce zbiórki;
- opis wymagań;
- status terminu.

Dla ograniczenia zakresu MVP jeden termin dotyczy jednego psa i jednej osoby wyprowadzającej.

System nie pozwala tworzyć nakładających się aktywnych terminów dla tego samego psa.

### BR-069 — Zgłoszenie użytkownika

Zalogowany użytkownik może zgłosić się na przyszły, otwarty termin.

Podaje dane kontaktowe, opcjonalną wiadomość oraz potwierdza zapoznanie się z wymaganiami.

Samo zgłoszenie nie oznacza rezerwacji ani zgody na spacer.

Użytkownik nie może mieć kilku aktywnych zgłoszeń na ten sam termin.

### BR-070 — Akceptacja i limit miejsc

Pracownik akceptuje lub odrzuca zgłoszenie.

Na jeden termin można zaakceptować najwyżej jednego użytkownika.

Po akceptacji:

- termin przestaje przyjmować nowe zgłoszenia;
- pozostałe oczekujące zgłoszenia są zamykane z informacją o zajęciu miejsca;
- zaakceptowany użytkownik otrzymuje potwierdzenie i instrukcje.

Użytkownik nie może mieć dwóch zaakceptowanych spacerów, których godziny się pokrywają.

### BR-071 — Statusy zgłoszenia i terminu

Zgłoszenie na spacer może mieć status:

- oczekujące;
- zaakceptowane;
- odrzucone;
- wycofane przez użytkownika;
- anulowane przez schronisko;
- zrealizowane;
- nieobecność.

Termin może być:

- otwarty;
- zarezerwowany;
- anulowany;
- zakończony.

Status realizacji lub nieobecności ustawia pracownik po planowanym terminie. Sam upływ czasu nie potwierdza odbycia spaceru.

### BR-072 — Rezygnacja i anulowanie

Użytkownik może wycofać przyszłe zgłoszenie, również zaakceptowane.

Schronisko otrzymuje informację o rezygnacji i może ponownie otworzyć termin. Wcześniej zamknięte zgłoszenia nie są automatycznie reaktywowane.

Schronisko może anulować termin z powodu np. zdrowia psa lub zmiany organizacji pracy.

Zmiana godzin lub psa w już zarezerwowanym terminie wymaga anulowania dotychczasowego terminu i opublikowania nowego. Użytkownik nie może zostać automatycznie przypisany do innego psa.

Adopcja lub wycofanie psa anuluje jego przyszłe aktywne terminy.

### BR-073 — Historia i powiadomienia

Użytkownik widzi własne zgłoszenia na spacery.

Pracownik widzi terminy, zgłoszenia i ich historię dla swojej placówki.

System wysyła powiadomienia o:

- nowym zgłoszeniu;
- akceptacji lub odrzuceniu;
- wycofaniu zgłoszenia;
- anulowaniu spaceru.

Dane uczestników spacerów nie są publiczne.

---

## 18. Reguły biznesowe

### RB-001

Tylko zatwierdzona i niezablokowana placówka może publikować karty zwierząt i oferty pomocy.

### RB-002

W MVP zwierzę jest przypisane do jednej placówki.

### RB-003

Nowe zgłoszenia adopcyjne można wysyłać wyłącznie do zwierząt dostępnych do adopcji.

### RB-004

Brak danych, odpowiedź negatywna i „nie dotyczy” są odrębnymi stanami.

### RB-005

Dopasowanie nie zatwierdza ani nie odrzuca kandydata.

### RB-006

Rozbieżność nie blokuje wysłania zgłoszenia adopcyjnego.

### RB-007

Zmiana profilu kandydata nie nadpisuje wcześniej wysłanych odpowiedzi.

### RB-008

Kandydat może mieć najwyżej jedno niezakończone zgłoszenie adopcyjne do danego zwierzęcia.

### RB-009

Kolejność zgłoszeń nie daje prawa do adopcji.

### RB-010

Zapis do ulubionych nie jest zgłoszeniem, rezerwacją ani wpłatą.

### RB-011

Adopcja kończy aktywną publikację i zamyka pozostałe niezakończone zgłoszenia adopcyjne do zwierzęcia.

### RB-012

Brak potwierdzenia aktualności nie oznacza, że zwierzę zostało adoptowane.

### RB-013

Wpłatę finansuje użytkownik. Kliknięcie przycisku nie powoduje wsparcia finansowanego przez portal lub sponsora.

### RB-014

Odbiorcą wpłaty jest podmiot przypisany do schroniska. Zwierzę może być celem wsparcia, ale nie osobnym odbiorcą.

### RB-015

Do statystyk trafiają wyłącznie potwierdzone wpłaty, z uwzględnieniem zwrotów.

### RB-016

Jedna wpłata dotycząca zwierzęcia jest uwzględniana raz w sumie wsparcia schroniska.

### RB-017

Kilka wpłat jednego użytkownika nie zwiększa liczby wspierających ponad jedną osobę w danym zakresie.

### RB-018

Wpłata nie daje pierwszeństwa w adopcji, wolontariacie ani zapisach na spacery.

### RB-019

Profil adopcyjny nie jest wymagany do wsparcia finansowego, wolontariatu ani spacerów.

### RB-020

Zgłoszenie do wolontariatu lub na spacer nie oznacza automatycznej akceptacji.

### RB-021

Na jeden termin spaceru można zaakceptować najwyżej jedną osobę.

### RB-022

Ten sam pies nie może mieć nakładających się aktywnych terminów spacerów, a użytkownik — nakładających się zaakceptowanych spacerów.

### RB-023

Rezygnacja ze spaceru nie reaktywuje automatycznie wcześniejszych zgłoszeń.

### RB-024

Adopcja lub wycofanie psa wyłącza nowe wpłaty wskazujące to zwierzę i anuluje jego przyszłe spacery, ale nie usuwa historii.

---

## 19. Przykładowe scenariusze biznesowe

### UC-001 — Znalezienie zwierzęcia

Gość wybiera gatunek, województwo i wielkość.

System prezentuje pasujące zwierzęta dostępne do adopcji.

Po otwarciu karty użytkownik widzi potrzeby, lokalizację, zasady adopcji i aktualność informacji.

### UC-002 — Przeglądanie schroniska

Użytkownik znajduje schronisko według miejscowości.

Otwiera profil placówki i przegląda jej podopiecznych oraz udostępnione formy pomocy.

### UC-003 — Dopasowanie przy brakujących danych

Kandydat deklaruje posiadanie kota.

Reakcja wybranego psa na koty jest nieznana.

System wskazuje brak danych i konieczność rozmowy, zamiast potwierdzać zgodność.

### UC-004 — Zgłoszenie mimo rozbieżności

Kandydat zapoznaje się z wyjaśnieniem i wysyła zgłoszenie.

Schronisko otrzymuje odpowiedzi, wynik porównania i wiadomość kandydata.

### UC-005 — Obsługa zgłoszenia adopcyjnego

Pracownik otwiera zgłoszenie dotyczące swojej placówki.

Zmienia status na „w kontakcie” i przekazuje informację o dalszych krokach.

Kandydat widzi zmianę i otrzymuje powiadomienie.

### UC-006 — Zakończenie adopcji

Pracownik oznacza zgłoszenie jako zakończone adopcją.

Zwierzę znika z aktywnych wyników, pozostali kandydaci otrzymują informację o zakończeniu ogłoszenia, a przyszłe spacery zostają anulowane.

### UC-007 — Potwierdzenie aktualności

Karta przekracza ustalony termin potwierdzenia.

System oznacza ją ostrzeżeniem.

Pracownik sprawdza dane i potwierdza aktualność, usuwając ostrzeżenie.

### UC-008 — Wsparcie wskazanego psa

Użytkownik otwiera kartę psa i wybiera „Nakarm psiaka”.

Wskazuje kwotę, zapoznaje się z odbiorcą i zasadami, a następnie dokonuje płatności u operatora.

Po potwierdzeniu wpłata pojawia się w jego historii, panelu schroniska i włączonych statystykach.

### UC-009 — Wsparcie całego schroniska

Użytkownik rozpoczyna płatność z profilu placówki bez wskazywania zwierzęcia.

Wpłata zwiększa wyłącznie statystyki ogólne schroniska.

### UC-010 — Nieudana lub zwrócona wpłata

Nieudana płatność nie zwiększa statystyk.

Po potwierdzonym zwrocie system aktualizuje kwotę wsparcia i odpowiednie liczniki.

### UC-011 — Zgłoszenie do wolontariatu

Użytkownik zapoznaje się z zasadami i przesyła formularz.

Pracownik kontaktuje się z nim, a następnie akceptuje lub odrzuca zgłoszenie.

Użytkownik widzi status i instrukcje dotyczące dalszych formalności.

### UC-012 — Zapis na spacer

Schronisko publikuje termin dla wskazanego psa.

Użytkownik przesyła zgłoszenie.

Pracownik akceptuje jedną osobę, a system zamyka pozostałe zgłoszenia i wysyła powiadomienia.

### UC-013 — Rezygnacja ze spaceru

Zaakceptowany użytkownik wycofuje zgłoszenie przed spacerem.

Schronisko otrzymuje informację i może ponownie otworzyć termin.

### UC-014 — Anulowanie przez schronisko

Schronisko anuluje spacer np. z powodu stanu zdrowia psa.

Zainteresowani otrzymują powiadomienie, a termin nie przyjmuje nowych zgłoszeń.

---

## 20. Zakres MVP

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
10. zgłoszenia adopcyjne;
11. obsługa i historia statusów;
12. potwierdzanie aktualności;
13. podstawowe powiadomienia e-mail;
14. moderacja i ograniczenia dostępu;
15. jednorazowe wsparcie finansowe w PLN;
16. integracja z jednym operatorem płatności;
17. historia wpłat użytkownika i panel schroniska;
18. zbiorcze statystyki wsparcia;
19. zgłoszenia do wolontariatu i ich obsługa;
20. publikowanie terminów spacerów;
21. zgłoszenia na spacery, akceptacje, rezygnacje i anulowanie.

Produkt powinien działać jako responsywna aplikacja webowa.

Dla zachowania zakresu:

- wpłaty wymagają konta;
- nie ma wpłat cyklicznych;
- jeden termin spaceru dotyczy jednego psa i jednej osoby;
- akceptacje są wykonywane ręcznie przez schronisko;
- nie powstaje pełny system kadrowy dla wolontariuszy;
- kontakt odbywa się przez statusy, krótkie wiadomości i e-mail.

Proponowany zakres demonstracyjny:

- 3–5 placówek;
- 30–50 kart zwierząt;
- konta demonstracyjne dla wszystkich ról;
- zgłoszenia adopcyjne i wolontariackie w różnych statusach;
- przykładowe terminy spacerów;
- płatności potwierdzone, nieudane i zwrócone w środowisku testowym operatora.

Demonstracja płatności testowych nie oznacza uruchomienia rzeczywistego przyjmowania pieniędzy.

Przed uruchomieniem produkcyjnym wymagane są rzeczywista konfiguracja odbiorców, uzgodnienia z operatorem i schroniskami oraz zatwierdzone zasady płatności, prywatności i obsługi zwrotów.

---

## 21. Poza zakresem MVP

Poza pierwszą wersją pozostają:

- objęcie wszystkich schronisk w Polsce;
- automatyczne pobieranie danych z innych stron;
- synchronizacja z zewnętrznymi systemami;
- mapa i filtrowanie według promienia odległości;
- natywna aplikacja mobilna;
- praca offline;
- pełna dokumentacja weterynaryjna;
- zarządzanie leczeniem i magazynem;
- pełne zarządzanie dyżurami, godzinami i dokumentacją wolontariuszy;
- generowanie i podpisywanie porozumień wolontariackich;
- obsługa spacerów grupowych;
- automatyczne przydzielanie wolontariuszy do psów;
- wpłaty cykliczne i subskrypcje;
- wiele walut;
- portfel użytkownika i przechowywanie środków przez portal;
- rozbudowane kampanie zbiórkowe z progami, nagrodami i budżetami;
- księgowość, fakturowanie i automatyczne zaświadczenia podatkowe;
- publiczne listy darczyńców;
- automatyczne raportowanie faktycznego wykorzystania każdej wpłaty;
- rozbudowany moduł inicjowania zwrotów w portalu;
- generowanie i podpisywanie umów adopcyjnych;
- rozbudowany czat;
- rezerwowanie wizyt adopcyjnych;
- automatyczne diagnozy;
- procentowe gwarancje dopasowania;
- automatyczna kwalifikacja kandydatów;
- transfery kart między placówkami.

---

## 22. Kryteria akceptacji MVP

### AC-001 — Wyszukiwanie

Można znaleźć zwierzęta, łącząc filtry gatunku, województwa, wieku i wielkości.

### AC-002 — Profil schroniska

Profil placówki pokazuje jej dane i opublikowane karty zgodnie z wybranym statusem.

### AC-003 — Karta zwierzęcia

Karta prezentuje dane podstawowe, zdjęcie, potrzeby, placówkę, status i aktualność.

### AC-004 — Zatwierdzenie placówki

Niezatwierdzone schronisko nie może opublikować karty ani oferty pomocy.

### AC-005 — Uprawnienia pracowników

Pracownik nie może odczytać ani zmienić niepublicznych danych innej placówki.

### AC-006 — Ulubione

Użytkownik może dodać i usunąć zwierzę z ulubionych bez tworzenia zgłoszenia.

### AC-007 — Kategorie dopasowania

System rozróżnia zgodność, rozbieżność, brak danych i „nie dotyczy”.

### AC-008 — Brak danych

Przy nieznanej reakcji psa na koty i obecności kota u kandydata system nie przedstawia zgodności.

### AC-009 — Wyjaśnienie

Wynik zawiera przyczyny, ale nie prezentuje gwarancji ani automatycznej decyzji o adopcji.

### AC-010 — Zgłoszenie mimo rozbieżności

Kandydat może wysłać zgłoszenie po zapoznaniu się z rozbieżnościami.

### AC-011 — Duplikaty zgłoszeń adopcyjnych

System blokuje drugie niezakończone zgłoszenie tej samej osoby do tego samego zwierzęcia.

### AC-012 — Zachowanie odpowiedzi

Zmiana profilu kandydata nie modyfikuje odpowiedzi w już wysłanym zgłoszeniu.

### AC-013 — Prywatność zgłoszeń

Kandydat widzi własne zgłoszenia, ale nie zgłoszenia innych osób.

### AC-014 — Historia statusów

Zmiana statusu zapisuje autora i datę oraz inicjuje odpowiednie powiadomienie.

### AC-015 — Adopcja

Oznaczenie adopcji usuwa zwierzę z aktywnych wyników i zamyka pozostałe niezakończone zgłoszenia adopcyjne.

### AC-016 — Nieaktualna karta

Po przekroczeniu progu aktualności pojawia się ostrzeżenie bez automatycznej zmiany statusu adopcji.

### AC-017 — Potwierdzenie aktualności

Potwierdzenie usuwa ostrzeżenie i zapisuje datę oraz osobę potwierdzającą.

### AC-018 — Wycofanie zgłoszenia adopcyjnego

Kandydat może wycofać własne niezakończone zgłoszenie.

### AC-019 — Brak ujawnienia danych

Publiczne widoki i powiadomienia nie ujawniają ankiet ani danych innych kandydatów, darczyńców i osób zgłaszających się do pomocy.

### AC-020 — Obsługa na telefonie

Wyszukiwanie, karta zwierzęcia, profil warunków, zgłoszenia i rozpoczęcie wpłaty są dostępne na urządzeniu mobilnym.

### AC-021 — Wybór wsparcia

Użytkownik może wybrać wsparcie placówki albo wskazanego zwierzęcia oraz sugerowaną lub własną kwotę.

### AC-022 — Jasny odbiorca i cel

Przed płatnością widoczne są kwota, odbiorca, cel i zasady wsparcia.

### AC-023 — Aktywacja płatności

Placówka bez aktywnego, zweryfikowanego odbiorcy nie może przyjmować wpłat.

### AC-024 — Potwierdzanie płatności

Samo przejście na stronę powrotu od operatora nie oznacza opłacenia. Potwierdzona informacja operatora aktualizuje status.

### AC-025 — Brak podwójnego naliczania

Powtórzone potwierdzenie tej samej płatności nie tworzy drugiej wpłaty ani nie zwiększa ponownie statystyk.

### AC-026 — Historia wpłat

Użytkownik widzi własną historię, a schronisko wpłaty dotyczące swojej placówki z rozróżnieniem celu i statusu.

### AC-027 — Statystyki wsparcia

Wpłaty oczekujące i nieudane nie zwiększają statystyk. Kolejne wpłaty tej samej osoby nie zwiększają liczby wspierających użytkowników.

### AC-028 — Zwroty

Potwierdzony częściowy lub pełny zwrot aktualizuje historię i statystyki zgodnie z BR-059.

### AC-029 — Brak profilu adopcyjnego

Użytkownik bez uzupełnionego profilu adopcyjnego może wpłacić środki i zgłosić się do pomocy.

### AC-030 — Formularz wolontariatu

Można wysłać zgłoszenie do placówki prowadzącej nabór i zobaczyć jego status.

### AC-031 — Obsługa wolontariatu

Pracownik może zaakceptować lub odrzucić zgłoszenie z zachowaniem historii i powiadomieniem użytkownika.

### AC-032 — Duplikaty wolontariatu

System blokuje kolejne aktywne zgłoszenie wolontariackie tej samej osoby do tej samej placówki.

### AC-033 — Publikacja spaceru

Pracownik może opublikować termin dla wskazanego psa z godzinami, miejscem zbiórki i wymaganiami.

### AC-034 — Brak nakładania terminów psa

System nie pozwala opublikować nakładających się aktywnych spacerów dla tego samego psa.

### AC-035 — Zgłoszenie na spacer

Użytkownik może zgłosić się na otwarty przyszły termin. Zgłoszenie nie oznacza jeszcze akceptacji.

### AC-036 — Limit akceptacji

Nie można zaakceptować więcej niż jednej osoby na termin, także gdy próby akceptacji następują równocześnie.

### AC-037 — Konflikt terminów użytkownika

Nie można zaakceptować użytkownika na dwa spacery o nakładających się godzinach.

### AC-038 — Rezygnacja

Użytkownik może zrezygnować z przyszłego spaceru. Schronisko otrzymuje powiadomienie i może ponownie otworzyć termin.

### AC-039 — Anulowanie spaceru

Schronisko może anulować termin. Zainteresowani otrzymują informację, a termin nie przyjmuje nowych zgłoszeń.

### AC-040 — Wpływ adopcji

Adopcja lub wycofanie psa wyłącza nowe wpłaty wskazujące to zwierzę i anuluje jego przyszłe aktywne spacery bez usuwania historii.

### AC-041 — Zmiana zarezerwowanego spaceru

Nie można po cichu zmienić psa lub godzin w zaakceptowanym terminie. Zmiana wymaga anulowania i nowego zgłoszenia.

### AC-042 — Rozdzielenie form pomocy

Wpłata nie zmienia statusu adopcji ani nie zatwierdza zgłoszenia do wolontariatu lub na spacer.

---

## 23. Kluczowe pytania otwarte

Do doprecyzowania przed realizacją:

1. Które schronisko skonsultuje pytania i reguły dopasowania?
2. Jak administrator potwierdza uprawnienie przedstawiciela placówki?
3. Czy w kolejnych wersjach obsługujemy fundacje i domy tymczasowe?
4. Jak definiujemy kategorie wielkości i poziomy aktywności?
5. Jak definiujemy poziomy doświadczenia kandydata?
6. Czy próg 30 dni na potwierdzenie aktualności odpowiada potrzebom placówek?
7. Jakie dane kontaktowe są niezbędne dla poszczególnych zgłoszeń?
8. Kto odpowiada za dane i jakie okresy przechowywania przyjmujemy?
9. Jak obsłużyć usunięcie konta z niezakończonym zgłoszeniem lub historią wpłat?
10. Czy placówki akceptują blokadę nowych zgłoszeń adopcyjnych przy statusie „proces adopcyjny w toku”?
11. Jakie materiały można wykorzystać w wersji demonstracyjnej?
12. Czy po zakończonym zgłoszeniu adopcyjnym można od razu wysłać kolejne?
13. Którego operatora płatności wybieramy?
14. Jaki podmiot będzie odbiorcą środków dla każdej placówki?
15. Kto ponosi prowizje i jak są one przedstawiane użytkownikowi?
16. Jakie są minimalne i maksymalne kwoty wpłat?
17. Jakie zasady dotyczą środków wskazujących zwierzę, którego potrzeby przestały być aktualne?
18. Kto obsługuje reklamacje i wnioski o zwrot?
19. Czy schroniska chcą publicznie pokazywać kwoty i liczbę wspierających?
20. Jakie wymagania wieku, szkolenia i formalności obowiązują wolontariuszy?
21. Czy spacer wymaga wcześniej zaakceptowanego zgłoszenia wolontariackiego?
22. Kto i jak potwierdza odbycie wdrożenia?
23. Jak długo przed spacerem użytkownik może samodzielnie wycofać zgłoszenie?
24. Czy dla projektu wystarcza zasada jednego psa i jednej osoby na termin?
25. Jakie warunki muszą być spełnione przed przejściem z płatności testowych na rzeczywiste?

---

## 24. Definicja sukcesu projektu

Projekt osiąga podstawowy cel, jeżeli kandydat do adopcji może:

1. znaleźć zwierzę odpowiadające podstawowym kryteriom;
2. poznać jego potrzeby i zasady adopcji;
3. zrozumieć zgodności, rozbieżności i brakujące informacje;
4. przesłać zgłoszenie do właściwego schroniska;
5. sprawdzić dalszy status zgłoszenia.

Osoba, która nie może adoptować zwierzęcia, powinna móc:

1. wesprzeć schronisko finansowo;
2. wskazać zwierzę jako cel wsparcia;
3. zobaczyć potwierdzoną wpłatę w historii;
4. zgłosić chęć udziału w wolontariacie;
5. zgłosić się na spacer;
6. otrzymać informację o decyzji schroniska i zmianach organizacyjnych.

Pracownik schroniska powinien móc:

1. opublikować i aktualizować kartę;
2. obsłużyć zgłoszenie adopcyjne;
3. zakończyć ogłoszenie po adopcji;
4. przeglądać wpłaty i ich cele;
5. obsługiwać zgłoszenia wolontariackie;
6. publikować terminy spacerów i decydować o zgłoszeniach;
7. zachować historię zgodnie z zasadami przechowywania danych.

Warunkiem odbioru projektu jest spełnienie kryteriów akceptacji na uzgodnionych danych testowych, w tym w środowisku testowym operatora płatności.

Warunkiem odbioru nie jest objęcie wszystkich schronisk w Polsce, uruchomienie rzeczywistych wpłat ani uzyskanie określonej liczby adopcji.
