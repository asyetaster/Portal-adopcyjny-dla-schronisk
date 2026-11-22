from sqlalchemy import text
from sqlalchemy.engine import Connection

from operations.animal.AddAnimalPhotoCommand import AddAnimalPhotoCommand
from operations.animal.CreateAnimalProfileCommand import CreateAnimalProfileCommand
from operations.animal.HideAnimalProfileCommand import HideAnimalProfileCommand
from operations.animal.PublishAnimalProfileCommand import PublishAnimalProfileCommand
from operations.animal.UpdateAnimalCareRequirementsCommand import (
    UpdateAnimalCareRequirementsCommand,
)
from operations.animal.UpdateAnimalProfileCommand import UpdateAnimalProfileCommand
from operations.animal.WithdrawAnimalProfileCommand import WithdrawAnimalProfileCommand
from operations.demo.animals import ANIMALS, PHOTOS

from operations.shelter.ApproveShelterRegistrationCommand import (
    ApproveShelterRegistrationCommand,
)
from operations.shelter.AssignShelterEmployeeCommand import AssignShelterEmployeeCommand
from operations.shelter.RejectShelterRegistrationCommand import (
    RejectShelterRegistrationCommand,
)
from operations.shelter.SubmitShelterRegistrationCommand import (
    SubmitShelterRegistrationCommand,
)
from operations.user.CreateUserCommand import CreateUserCommand

DEMO_PASSWORD = "demo1234"

USERS = [
    # (email, imię, nazwisko, admin)
    ("admin@demo.pl", "Adam", "Administrator", True),
    ("pracownik1@demo.pl", "Paula", "Pracowniczka", False),
    ("pracowniczka1@demo.pl", "Laura", "Pracowniczka", False),
    ("pracownik2@demo.pl", "Piotr", "Pracowniczy", False),
    ("anna@demo.pl", "Anna", "Nowak", False),
    ("jan@demo.pl", "Jan", "Kowalski", False),
    ("ewa@demo.pl", "Ewa", "Wiśniewska", False),
    ("karol@demo.pl", "Karol", "Wiśniewska", False),
    ("magda.zielinska@demo.example", "Magdalena", "Zielińska", False),
    ("tomasz.wrobel@demo.example", "Tomasz", "Wróbel", False),
    ("aleksandra.mazur@demo.example", "Aleksandra", "Mazur", False),
    ("michal.krawczyk@demo.example", "Michał", "Krawczyk", False),
    ("natalia.kaczmarek@demo.example", "Natalia", "Kaczmarek", False),
    ("pawel.lewandowski@demo.example", "Paweł", "Lewandowski", False),
    ("joanna.dabrowska@demo.example", "Joanna", "Dąbrowska", False),
    ("krzysztof.wozniak@demo.example", "Krzysztof", "Woźniak", False),
    ("monika.kozlowska@demo.example", "Monika", "Kozłowska", False),
    ("marcin.jankowski@demo.example", "Marcin", "Jankowski", False),
    ("agnieszka.wojciechowska@demo.example", "Agnieszka", "Wojciechowska", False),
    ("lukasz.kwiatkowski@demo.example", "Łukasz", "Kwiatkowski", False),
    ("karolina.kaminska@demo.example", "Karolina", "Kamińska", False),
    ("mateusz.piotrowski@demo.example", "Mateusz", "Piotrowski", False),
    ("patrycja.grabowska@demo.example", "Patrycja", "Grabowska", False),
    ("bartosz.pawlak@demo.example", "Bartosz", "Pawlak", False),
    ("dorota.michalska@demo.example", "Dorota", "Michalska", False),
    ("rafal.krol@demo.example", "Rafał", "Król", False),
    ("sylwia.wieczorek@demo.example", "Sylwia", "Wieczorek", False),
    ("jakub.jablonski@demo.example", "Jakub", "Jabłoński", False),
    ("justyna.nowakowska@demo.example", "Justyna", "Nowakowska", False),
    ("damian.olszewski@demo.example", "Damian", "Olszewski", False),
    ("weronika.stasiak@demo.example", "Weronika", "Stasiak", False),
    ("adrian.dudek@demo.example", "Adrian", "Dudek", False),
    ("klaudia.walczak@demo.example", "Klaudia", "Walczak", False),
    ("sebastian.sikora@demo.example", "Sebastian", "Sikora", False),
    ("alina.baranska@demo.example", "Alina", "Barańska", False),
    ("grzegorz.lis@demo.example", "Grzegorz", "Lis", False),
    ("renata.sadowska@demo.example", "Renata", "Sadowska", False),
    ("filip.czarnecki@demo.example", "Filip", "Czarnecki", False),
]

SHELTERS = [
    # (zgłaszający, dane, status docelowy, dodatkowi pracownicy)
    (
        "pracownik1@demo.pl",
        dict(
            name="Schronisko „Przyjazna Łapa”",
            street_address="ul. Leśna 12",
            postal_code="00-950",
            city="Warszawa",
            voivodeship="mazowieckie",
            contact_email="kontakt@przyjaznalapa.example",
            contact_phone="22 123 45 67",
            website="https://przyjaznalapa.example",
            description="Miejskie schronisko dla psów i kotów. Około 120 podopiecznych.",
            adoption_rules="Wizyta zapoznawcza, umowa adopcyjna, wizyta poadopcyjna po miesiącu.",
        ),
        "Approved",
        ["pracownik2@demo.pl"],
    ),
    (
        "pracowniczka1@demo.pl",
        dict(
            name="Schronisko „Psisko”",
            street_address="ul. Kwiatowa 34",
            postal_code="90-950",
            city="Łódź",
            voivodeship="łódzkie",
            contact_email="kontakt@psisko.example",
            contact_phone="22 123 45 67",
            website="https://przyjaznalapa.example",
            description="Miejskie schronisko dla psów i kotów. Około 120 podopiecznych.",
            adoption_rules="Wizyta zapoznawcza, umowa adopcyjna, wizyta poadopcyjna po miesiącu.",
        ),
        "Approved",
        [],
    ),
    (
        "pracownik2@demo.pl",
        dict(
            name="Fundacja Kocie Serce",
            street_address="ul. Floriańska 5",
            postal_code="31-019",
            city="Kraków",
            voivodeship="małopolskie",
            contact_email="adopcje@kocieserce.example",
            description="Dom tymczasowy dla kotów, specjalizujemy się w kotach seniorach.",
            adoption_rules="Ankieta przedadopcyjna i siatka w oknach.",
        ),
        "Approved",
        [],
    ),
    (
        "anna@demo.pl",
        dict(
            name="Azyl pod Dębem",
            street_address="ul. Polna 3",
            postal_code="80-001",
            city="Gdańsk",
            voivodeship="pomorskie",
            contact_email="azyl@podebem.example",
        ),
        "Pending",
        [],
    ),
    (
        "jan@demo.pl",
        dict(
            name="Psia Przystań",
            street_address="ul. Ogrodowa 8",
            postal_code="50-001",
            city="Wrocław",
            voivodeship="dolnośląskie",
            contact_email="psiaprzystan@example.com",
        ),
        "Rejected",
        [],
    ),
    (
        "magda.zielinska@demo.example",
        dict(
            name="Schronisko „Leśna Przystań”",
            street_address="ul. Paprociowa 18",
            postal_code="85-001",
            city="Bydgoszcz",
            voivodeship="kujawsko-pomorskie",
            contact_email="kontakt@lesnaprzystan.example",
            contact_phone="000 000 101",
            website="https://lesnaprzystan.example",
            description="Schronisko dla psów i kotów z wybiegiem i strefą socjalizacji.",
            adoption_rules="Ankieta, spacer zapoznawczy i podpisanie umowy adopcyjnej.",
        ),
        "Approved",
        [],
    ),
    (
        "tomasz.wrobel@demo.example",
        dict(
            name="Fundacja „Mruczący Zakątek”",
            street_address="ul. Lawendowa 7",
            postal_code="31-001",
            city="Kraków",
            voivodeship="małopolskie",
            contact_email="adopcje@mruczacyzakatek.example",
            contact_phone="000 000 102",
            website="https://mruczacyzakatek.example",
            description="Sieć domów tymczasowych dla kotów, w tym kociąt wymagających opieki.",
            adoption_rules="Rozmowa, zabezpieczenie okien i balkonu oraz umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "aleksandra.mazur@demo.example",
        dict(
            name="Schronisko „Nadmorska Łapa”",
            street_address="ul. Wydmowa 24",
            postal_code="80-001",
            city="Gdańsk",
            voivodeship="pomorskie",
            contact_email="biuro@nadmorskalapa.example",
            contact_phone="000 000 103",
            website="https://nadmorskalapa.example",
            description="Ośrodek dla bezdomnych zwierząt prowadzący program spacerów wolontariackich.",
            adoption_rules="Dwa spotkania ze zwierzęciem, rozmowa z opiekunem i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "michal.krawczyk@demo.example",
        dict(
            name="Fundacja „Drugi Start”",
            street_address="ul. Pogodna 11",
            postal_code="50-001",
            city="Wrocław",
            voivodeship="dolnośląskie",
            contact_email="pomoc@drugistart.example",
            contact_phone="000 000 104",
            website="https://drugistart.example",
            description="Fundacja wspierająca psy po urazach i zabiegach ortopedycznych.",
            adoption_rules="Konsultacja z opiekunem, omówienie rehabilitacji i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "natalia.kaczmarek@demo.example",
        dict(
            name="Schronisko „Pod Dobrym Dachem”",
            street_address="ul. Polna 36",
            postal_code="60-001",
            city="Poznań",
            voivodeship="wielkopolskie",
            contact_email="kontakt@poddobrymdachem.example",
            contact_phone="000 000 105",
            website="https://poddobrymdachem.example",
            description="Schronisko z oddzielnymi strefami dla szczeniąt, dorosłych psów i seniorów.",
            adoption_rules="Ankieta, spotkanie zapoznawcze i podpisanie umowy.",
        ),
        "Approved",
        [],
    ),
    (
        "pawel.lewandowski@demo.example",
        dict(
            name="Fundacja „Uszata Polana”",
            street_address="ul. Koniczynowa 5",
            postal_code="90-001",
            city="Łódź",
            voivodeship="łódzkie",
            contact_email="adopcje@uszatapolana.example",
            contact_phone="000 000 106",
            website="https://uszatapolana.example",
            description="Fundacja zajmująca się królikami i edukacją ich przyszłych opiekunów.",
            adoption_rules="Ankieta, przygotowanie bezpiecznej przestrzeni i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "joanna.dabrowska@demo.example",
        dict(
            name="Schronisko „Ciepły Kąt”",
            street_address="ul. Brzozowa 42",
            postal_code="20-001",
            city="Lublin",
            voivodeship="lubelskie",
            contact_email="biuro@cieplykat.example",
            contact_phone="000 000 107",
            website="https://cieplykat.example",
            description="Placówka dla psów i kotów prowadząca także poszukiwania ich właścicieli.",
            adoption_rules="Rozmowa z pracownikiem, zapoznanie ze zwierzęciem i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "krzysztof.wozniak@demo.example",
        dict(
            name="Fundacja „Psia Jesień”",
            street_address="ul. Kasztanowa 9",
            postal_code="70-001",
            city="Szczecin",
            voivodeship="zachodniopomorskie",
            contact_email="kontakt@psiajesien.example",
            contact_phone="000 000 108",
            website="https://psiajesien.example",
            description="Domy tymczasowe i opieka weterynaryjna dla starszych psów.",
            adoption_rules="Rozmowa o potrzebach seniora, wizyta przedadopcyjna i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "monika.kozlowska@demo.example",
        dict(
            name="Schronisko „Zielone Wzgórze”",
            street_address="ul. Wzgórze 15",
            postal_code="15-001",
            city="Białystok",
            voivodeship="podlaskie",
            contact_email="adopcje@zielonewzgorze.example",
            contact_phone="000 000 109",
            website="https://zielonewzgorze.example",
            description="Schronisko z programem pracy behawioralnej dla psów lękliwych.",
            adoption_rules="Spotkanie z opiekunem, spacery zapoznawcze i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "marcin.jankowski@demo.example",
        dict(
            name="Fundacja „Koci Kompas”",
            street_address="ul. Słoneczna 28",
            postal_code="40-001",
            city="Katowice",
            voivodeship="śląskie",
            contact_email="kontakt@kocikompas.example",
            contact_phone="000 000 110",
            website="https://kocikompas.example",
            description="Fundacja pomagająca kotom porzuconym i organizująca domy tymczasowe.",
            adoption_rules="Ankieta, rozmowa telefoniczna, zabezpieczenie okien i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "agnieszka.wojciechowska@demo.example",
        dict(
            name="Schronisko „Bezpieczna Polana”",
            street_address="ul. Sosnowa 13",
            postal_code="25-001",
            city="Kielce",
            voivodeship="świętokrzyskie",
            contact_email="biuro@bezpiecznapolana.example",
            contact_phone="000 000 111",
            website="https://bezpiecznapolana.example",
            description="Schronisko dla zwierząt z terenów miejskich i okolicznych gmin.",
            adoption_rules="Ankieta adopcyjna, spotkanie na miejscu i podpisanie umowy.",
        ),
        "Approved",
        [],
    ),
    (
        "lukasz.kwiatkowski@demo.example",
        dict(
            name="Fundacja „Cztery Łapy Razem”",
            street_address="ul. Rumiankowa 6",
            postal_code="35-001",
            city="Rzeszów",
            voivodeship="podkarpackie",
            contact_email="pomoc@czterylapyrazem.example",
            contact_phone="000 000 112",
            website="https://czterylapyrazem.example",
            description="Fundacja szukająca wspólnych domów dla zaprzyjaźnionych par zwierząt.",
            adoption_rules="Rozmowa, zapoznanie z obojgiem zwierząt i wspólna umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "karolina.kaminska@demo.example",
        dict(
            name="Schronisko „Mazurski Azyl”",
            street_address="ul. Jeziorna 31",
            postal_code="10-001",
            city="Olsztyn",
            voivodeship="warmińsko-mazurskie",
            contact_email="kontakt@mazurskiazyl.example",
            contact_phone="000 000 113",
            website="https://mazurskiazyl.example",
            description="Kameralne schronisko dla psów z rozległym terenem spacerowym.",
            adoption_rules="Spacer zapoznawczy, rozmowa o warunkach opieki i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "mateusz.piotrowski@demo.example",
        dict(
            name="Fundacja „Małe Serca”",
            street_address="ul. Fiołkowa 4",
            postal_code="45-001",
            city="Opole",
            voivodeship="opolskie",
            contact_email="adopcje@maleserca.example",
            contact_phone="000 000 114",
            website="https://maleserca.example",
            description="Fundacja dla małych ssaków: świnek morskich, chomików i szczurów.",
            adoption_rules="Ankieta, omówienie warunków utrzymania danego gatunku i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "patrycja.grabowska@demo.example",
        dict(
            name="Schronisko „Sosnowy Dom”",
            street_address="ul. Szyszkowa 22",
            postal_code="65-001",
            city="Zielona Góra",
            voivodeship="lubuskie",
            contact_email="biuro@sosnowydom.example",
            contact_phone="000 000 115",
            website="https://sosnowydom.example",
            description="Schronisko prowadzące adopcje psów oraz zajęcia edukacyjne dla szkół.",
            adoption_rules="Spotkanie z opiekunem, spacer i podpisanie umowy adopcyjnej.",
        ),
        "Approved",
        [],
    ),
    (
        "bartosz.pawlak@demo.example",
        dict(
            name="Fundacja „Most do Domu”",
            street_address="ul. Mostowa 17",
            postal_code="89-600",
            city="Chojnice",
            voivodeship="pomorskie",
            contact_email="kontakt@mostdodomu.example",
            contact_phone="000 000 116",
            website="https://mostdodomu.example",
            description="Sieć domów tymczasowych przygotowujących psy do życia w mieszkaniu.",
            adoption_rules="Ankieta, spotkanie w domu tymczasowym i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "dorota.michalska@demo.example",
        dict(
            name="Schronisko „Bursztynowa Przystań”",
            street_address="ul. Muszlowa 8",
            postal_code="81-001",
            city="Gdynia",
            voivodeship="pomorskie",
            contact_email="adopcje@bursztynowaprzystan.example",
            contact_phone="000 000 117",
            website="https://bursztynowaprzystan.example",
            description="Schronisko dla psów i kotów z pokojami do spotkań adopcyjnych.",
            adoption_rules="Rozmowa z pracownikiem, spotkanie ze zwierzęciem i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "rafal.krol@demo.example",
        dict(
            name="Fundacja „Odważny Ogon”",
            street_address="ul. Spokojna 19",
            postal_code="26-600",
            city="Radom",
            voivodeship="mazowieckie",
            contact_email="pomoc@odwaznyogon.example",
            contact_phone="000 000 118",
            website="https://odwaznyogon.example",
            description="Pomoc psom wymagającym socjalizacji i stopniowego oswajania z ludźmi.",
            adoption_rules="Cykl spotkań, konsultacja behawioralna i podpisanie umowy.",
        ),
        "Approved",
        [],
    ),
    (
        "sylwia.wieczorek@demo.example",
        dict(
            name="Schronisko „Jurajska Łapa”",
            street_address="ul. Skalna 27",
            postal_code="42-200",
            city="Częstochowa",
            voivodeship="śląskie",
            contact_email="kontakt@jurajskalapa.example",
            contact_phone="000 000 119",
            website="https://jurajskalapa.example",
            description="Schronisko organizujące spacery terenowe i adopcje psów aktywnych.",
            adoption_rules="Ankieta, wspólny spacer i omówienie potrzeb ruchowych psa.",
        ),
        "Approved",
        [],
    ),
    (
        "jakub.jablonski@demo.example",
        dict(
            name="Fundacja „Kocia Przystań”",
            street_address="ul. Jaśminowa 10",
            postal_code="09-400",
            city="Płock",
            voivodeship="mazowieckie",
            contact_email="adopcje@kociaprzystan.example",
            contact_phone="000 000 120",
            website="https://kociaprzystan.example",
            description="Fundacja zapewniająca opiekę kotom dorosłym i kocim seniorom.",
            adoption_rules="Rozmowa, zabezpieczenie mieszkania i podpisanie umowy.",
        ),
        "Approved",
        [],
    ),
    (
        "justyna.nowakowska@demo.example",
        dict(
            name="Schronisko „Sudecki Przyjaciel”",
            street_address="ul. Górska 33",
            postal_code="58-300",
            city="Wałbrzych",
            voivodeship="dolnośląskie",
            contact_email="biuro@sudeckiprzyjaciel.example",
            contact_phone="000 000 121",
            website="https://sudeckiprzyjaciel.example",
            description="Schronisko dla psów prowadzące program adopcji wspieranych.",
            adoption_rules="Spotkania zapoznawcze, ustalenie zakresu wsparcia i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "damian.olszewski@demo.example",
        dict(
            name="Fundacja „Nowa Smycz”",
            street_address="ul. Wiosenna 14",
            postal_code="75-001",
            city="Koszalin",
            voivodeship="zachodniopomorskie",
            contact_email="kontakt@nowasmycz.example",
            contact_phone="000 000 122",
            website="https://nowasmycz.example",
            description="Fundacja pomagająca porzuconym psom i wspierająca rodziny adopcyjne.",
            adoption_rules="Ankieta, spacer, rozmowa z domownikami i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "weronika.stasiak@demo.example",
        dict(
            name="Schronisko „Dolina Ogonów”",
            street_address="ul. Dolinna 21",
            postal_code="33-300",
            city="Nowy Sącz",
            voivodeship="małopolskie",
            contact_email="adopcje@dolinaogonow.example",
            contact_phone="000 000 123",
            website="https://dolinaogonow.example",
            description="Schronisko dla psów i kotów z programem wolontariatu rodzinnego.",
            adoption_rules="Wizyta zapoznawcza wszystkich domowników i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "adrian.dudek@demo.example",
        dict(
            name="Fundacja „Puchaty Patrol”",
            street_address="ul. Akacjowa 16",
            postal_code="62-800",
            city="Kalisz",
            voivodeship="wielkopolskie",
            contact_email="pomoc@puchatypatrol.example",
            contact_phone="000 000 124",
            website="https://puchatypatrol.example",
            description="Fundacja organizująca leczenie i domy tymczasowe dla znalezionych kotów.",
            adoption_rules="Ankieta, rozmowa z opiekunem tymczasowym i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "klaudia.walczak@demo.example",
        dict(
            name="Schronisko „Wierny Towarzysz”",
            street_address="ul. Lipowa 39",
            postal_code="82-300",
            city="Elbląg",
            voivodeship="warmińsko-mazurskie",
            contact_email="kontakt@wiernytowarzysz.example",
            contact_phone="000 000 125",
            website="https://wiernytowarzysz.example",
            description="Schronisko dobierające psy do trybu życia i doświadczenia opiekunów.",
            adoption_rules="Rozmowa o trybie życia, spotkanie z psem i podpisanie umowy.",
        ),
        "Approved",
        [],
    ),
    (
        "sebastian.sikora@demo.example",
        dict(
            name="Fundacja „Łapa w Dłoń”",
            street_address="ul. Ogrodowa 23",
            postal_code="08-110",
            city="Siedlce",
            voivodeship="mazowieckie",
            contact_email="biuro@lapawdlon.example",
            contact_phone="000 000 126",
            website="https://lapawdlon.example",
            description="Fundacja wspierająca adopcje zwierząt dorosłych i ich adaptację w domu.",
            adoption_rules="Ankieta, spotkanie zapoznawcze i uzgodnienie kontaktu poadopcyjnego.",
        ),
        "Approved",
        [],
    ),
    (
        "alina.baranska@demo.example",
        dict(
            name="Schronisko „Cicha Łąka”",
            street_address="ul. Łąkowa 12",
            postal_code="22-400",
            city="Zamość",
            voivodeship="lubelskie",
            contact_email="adopcje@cichalaka.example",
            contact_phone="000 000 127",
            website="https://cichalaka.example",
            description="Niewielkie schronisko zapewniające spokojne warunki psom i kotom.",
            adoption_rules="Wizyta w schronisku, rozmowa z opiekunem i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "grzegorz.lis@demo.example",
        dict(
            name="Fundacja „MerdaMY”",
            street_address="ul. Klonowa 30",
            postal_code="44-100",
            city="Gliwice",
            voivodeship="śląskie",
            contact_email="kontakt@merdamy.example",
            contact_phone="000 000 128",
            website="https://merdamy.example",
            description="Fundacja prowadząca domy tymczasowe dla szczeniąt i młodych psów.",
            adoption_rules="Ankieta, omówienie wychowania młodego psa i umowa adopcyjna.",
        ),
        "Approved",
        [],
    ),
    (
        "renata.sadowska@demo.example",
        dict(
            name="Schronisko „Przystanek Dom”",
            street_address="ul. Wrzosowa 25",
            postal_code="97-300",
            city="Piotrków Trybunalski",
            voivodeship="łódzkie",
            contact_email="biuro@przystanekdom.example",
            contact_phone="000 000 129",
            website="https://przystanekdom.example",
            description="Schronisko z programem przygotowania zwierząt do pierwszej adopcji.",
            adoption_rules="Spotkanie informacyjne, zapoznanie ze zwierzęciem i umowa.",
        ),
        "Approved",
        [],
    ),
    (
        "filip.czarnecki@demo.example",
        dict(
            name="Fundacja „Pod Jednym Kocem”",
            street_address="ul. Malinowa 3",
            postal_code="66-400",
            city="Gorzów Wielkopolski",
            voivodeship="lubuskie",
            contact_email="adopcje@podjednymkocem.example",
            contact_phone="000 000 130",
            website="https://podjednymkocem.example",
            description="Fundacja szukająca domów dla psów i kotów przyzwyczajonych do innych zwierząt.",
            adoption_rules="Rozmowa, kontrolowane zapoznanie ze zwierzętami rezydentami i umowa.",
        ),
        "Approved",
        [],
    ),
]


class SeedDemoDataCommand:
    """Wypełnia bazę danymi demo (konta z hasłem demo1234, placówki). Idempotentny."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self) -> dict:
        ids = self._seed_users()
        shelters = self._seed_shelters(ids)
        animals = self._seed_animals(ids)
        return {"users": len(ids), "shelters": shelters, "animals": animals}

    def _seed_users(self) -> dict[str, int]:
        ids = {}
        create = CreateUserCommand(self.connection)
        for email, first_name, last_name, is_admin in USERS:
            existing = self.connection.execute(
                text("SELECT id FROM users WHERE email = :email"), {"email": email}
            ).scalar_one_or_none()
            ids[email] = existing or create.execute(
                email=email,
                password=DEMO_PASSWORD,
                first_name=first_name,
                last_name=last_name,
                is_admin=is_admin,
            )
        return ids

    def _seed_shelters(self, ids: dict[str, int]) -> int:
        admin_id = ids["admin@demo.pl"]
        created = 0
        for submitter, data, status, employees in SHELTERS:
            exists = self.connection.execute(
                text("SELECT 1 FROM shelters WHERE name = :name"), {"name": data["name"]}
            ).first()
            if exists:
                continue

            shelter_id = SubmitShelterRegistrationCommand(self.connection).execute(
                actor_id=ids[submitter], **data
            )
            if status == "Approved":
                ApproveShelterRegistrationCommand(self.connection).execute(
                    actor_id=admin_id, shelter_id=shelter_id
                )
            elif status == "Rejected":
                RejectShelterRegistrationCommand(self.connection).execute(
                    actor_id=admin_id,
                    shelter_id=shelter_id,
                    reason="Brak numeru telefonu i opisu placówki. Uzupełnij dane.",
                )
            for email in employees:
                AssignShelterEmployeeCommand(self.connection).execute(
                    actor_id=ids[submitter], shelter_id=shelter_id, email=email
                )
            created += 1
        return created
    
    def _seed_animals(self, ids: dict[str, int]) -> int:
        """Karty demo w różnych stanach (M3). Pomija karty, które już istnieją."""
        admin_id = ids["admin@demo.pl"]
        created = 0
        for shelter_name, author, data, requirements, state in ANIMALS:
            shelter_id = self.connection.execute(
                text("SELECT id FROM shelters WHERE name = :name"), {"name": shelter_name}
            ).scalar_one_or_none()
            if shelter_id is None:
                continue
            exists = self.connection.execute(
                text("SELECT 1 FROM animals WHERE shelter_id = :s AND name = :n"),
                {"s": shelter_id, "n": data["name"]},
            ).first()
            if exists:
                continue

            actor_id = ids[author]
            animal_id = CreateAnimalProfileCommand(self.connection).execute(
                actor_id=actor_id, shelter_id=shelter_id,
                name=data["name"], species=data["species"],
            )
            UpdateAnimalProfileCommand(self.connection).execute(
                actor_id=actor_id, shelter_id=shelter_id, animal_id=animal_id, **data
            )
            if requirements:
                UpdateAnimalCareRequirementsCommand(self.connection).execute(
                    actor_id=actor_id, shelter_id=shelter_id, animal_id=animal_id, **requirements
                )
            if state != "draft":
                AddAnimalPhotoCommand(self.connection).execute(
                    actor_id=actor_id, shelter_id=shelter_id, animal_id=animal_id,
                    file_path=PHOTOS[data["species"]], alt_text=f"Zdjęcie poglądowe: {data['name']}",
                )
                PublishAnimalProfileCommand(self.connection).execute(
                    actor_id=actor_id, shelter_id=shelter_id, animal_id=animal_id
                )
            self._apply_state(state, animal_id, shelter_id, actor_id, admin_id)
            created += 1
        return created

    def _apply_state(self, state: str, animal_id: int, shelter_id: int, actor_id: int, admin_id: int) -> None:
        if state == "stale":
            # Ostatnie potwierdzenie 40 dni temu: karta z ostrzeżeniem (BR-045).
            self.connection.execute(
                text("""UPDATE animals SET last_confirmed_at =
                        strftime('%Y-%m-%dT%H:%M:%SZ', 'now', '-40 days') WHERE id = :id"""),
                {"id": animal_id},
            )
        elif state == "in_progress":
            # Prawdziwe przejście robi StartAnimalAdoptionProcessCommand (M5);
            # do tego czasu ustawiamy status wprost.
            self.connection.execute(
                text("UPDATE animals SET status = 'AdoptionInProgress' WHERE id = :id"),
                {"id": animal_id},
            )
        elif state == "withdrawn":
            WithdrawAnimalProfileCommand(self.connection).execute(
                actor_id=actor_id, shelter_id=shelter_id, animal_id=animal_id,
                reason="Adopcja poza portalem.",
            )
        elif state == "hidden":
            HideAnimalProfileCommand(self.connection).execute(
                actor_id=admin_id, animal_id=animal_id, reason="Do wyjaśnienia (dane demo).",
            )
