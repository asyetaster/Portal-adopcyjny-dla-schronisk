"""Dane demo kart zwierząt (M3). Wszystko fikcyjne (BR-047).

Każdy wpis: (placówka, autor, dane karty, wymagania, stan).
Stany: ``available``, ``stale`` (bez potwierdzenia od 40 dni), ``in_progress``,
``draft``, ``withdrawn``, ``hidden`` (ukryta przez administratora).
"""

PRZYJAZNA = "Schronisko „Przyjazna Łapa”"
PSISKO = "Schronisko „Psisko”"
KOCIE_SERCE = "Fundacja Kocie Serce"

PHOTOS = {"Dog": "img/demo-dog.svg", "Cat": "img/demo-cat.svg"}

NO_DATA = dict(
    good_with_children="Unknown", good_with_dogs="Unknown",
    good_with_cats="Unknown", special_care_required="Unknown",
)


def _req(children="Unknown", dogs="Unknown", cats="Unknown", care="Unknown", **extra):
    return dict(
        good_with_children=children, good_with_dogs=dogs, good_with_cats=cats,
        special_care_required=care, **extra,
    )


ANIMALS = [
    (PRZYJAZNA, "pracownik1@demo.pl", dict(
        name="Burek", species="Dog", sex="Male", breed="Mieszaniec", size="Medium",
        age_min_months=24, age_max_months=36, temperament="łagodny,towarzyski",
        description="Spokojny pies, który uwielbia długie spacery i głaskanie za uchem.",
        daily_needs="Dwa spacery dziennie, karma sucha, bez diety."),
     _req("Yes", "Yes", "No", "No", activity_level="Medium", min_experience="Basic"), "available"),
    (PRZYJAZNA, "pracownik1@demo.pl", dict(
        name="Luna", species="Dog", sex="Female", breed="Labrador", size="Large",
        age_min_months=48, age_max_months=60, temperament="energiczna,radosna",
        description="Energiczna suczka, szukająca aktywnego opiekuna z ogrodem.",
        daily_needs="Długie spacery, zabawy z piłką, karma bytowa."),
     _req("Yes", "Unknown", "Unknown", "No", activity_level="High", min_experience="Experienced"), "available"),
    (PRZYJAZNA, "pracownik2@demo.pl", dict(
        name="Maks", species="Dog", sex="Male", breed="Jamnik", size="Small",
        age_min_months=6, age_max_months=12, temperament="ciekawski",
        description="Młody psiak, dopiero uczy się chodzenia na smyczy.",
        daily_needs="Trzy krótkie spacery, szkolenie podstawowe."),
     _req("Unknown", "Yes", "Unknown", "No", activity_level="Medium", min_experience="None"), "available"),
    (PRZYJAZNA, "pracownik1@demo.pl", dict(
        name="Reksio", species="Dog", sex="Male", breed="Owczarek", size="Large",
        age_min_months=84, age_max_months=96, temperament="spokojny",
        description="Senior o wielkim sercu. Lubi leżeć obok człowieka.",
        daily_needs="Krótkie spacery, leki na stawy raz dziennie."),
     _req("Yes", "Yes", "Yes", "Yes", special_care_notes="Preparat na stawy rano.", min_experience="Basic"), "stale"),
    (PRZYJAZNA, "pracownik1@demo.pl", dict(
        name="Azor", species="Dog", sex="Male", breed="Mieszaniec", size="Medium",
        age_min_months=36, age_max_months=48, temperament="lojalny",
        description="Pies, z którym wstępnie dogadaliśmy się z kandydatem.",
        daily_needs="Dwa spacery dziennie."),
     _req("Yes", "No", "No", "No"), "in_progress"),
    (PRZYJAZNA, "pracownik1@demo.pl", dict(
        name="Szkicownik", species="Dog", sex="Unknown", description="", daily_needs=""),
     None, "draft"),
    (PSISKO, "pracowniczka1@demo.pl", dict(
        name="Bella", species="Dog", sex="Female", breed="Beagle", size="Medium",
        age_min_months=18, age_max_months=24, temperament="wesoła,uparta",
        description="Beagle z charakterem. Świetnie węszy i uwielbia nagrody.",
        daily_needs="Trzy spacery, kontrola porcji jedzenia."),
     _req("Yes", "Yes", "Unknown", "No", activity_level="High", min_experience="Basic"), "available"),
    (PSISKO, "pracowniczka1@demo.pl", dict(
        name="Rocky", species="Dog", sex="Male", breed="Bokser", size="Large",
        age_min_months=60, age_max_months=72, temperament="silny,oddany",
        description="Spokojny w domu, ciągnie na smyczy. Potrzebuje cierpliwego opiekuna.",
        daily_needs="Dwa solidne spacery, trening smyczy."),
     _req("Unknown", "No", "No", "No", activity_level="High", min_experience="Experienced"), "available"),
    (PSISKO, "pracowniczka1@demo.pl", dict(
        name="Pimpek", species="Dog", sex="Male", breed="Mieszaniec", size="Small",
        age_min_months=12, age_max_months=24, temperament="towarzyski",
        description="Karta wycofana po adopcji poza portalem.",
        daily_needs="Dwa spacery."),
     _req("Yes", "Yes", "Yes", "No"), "withdrawn"),
    (PSISKO, "pracowniczka1@demo.pl", dict(
        name="Sporny", species="Dog", sex="Male", breed="Mieszaniec", size="Medium",
        age_min_months=30, age_max_months=40, temperament="",
        description="Karta ukryta przez administratora do wyjaśnienia (dane demo).",
        daily_needs="Dwa spacery."),
     None, "hidden"),
    (KOCIE_SERCE, "pracownik2@demo.pl", dict(
        name="Mruczek", species="Cat", sex="Male", breed="Europejski", size="Small",
        age_min_months=36, age_max_months=48, temperament="pieszczoch,spokojny",
        description="Kot kanapowy. Mruczy od progu i wskakuje na kolana.",
        daily_needs="Sucha i mokra karma, czysta kuweta."),
     _req("Yes", "Unknown", "Yes", "No", activity_level="Low", min_experience="None"), "available"),
    (KOCIE_SERCE, "pracownik2@demo.pl", dict(
        name="Pani Futerko", species="Cat", sex="Female", breed="Perska", size="Small",
        age_min_months=60, age_max_months=72, temperament="dostojna",
        description="Perska dama, wymaga codziennego szczotkowania.",
        daily_needs="Szczotkowanie, karma mokra dwa razy dziennie."),
     _req("No", "Unknown", "Unknown", "Yes", special_care_notes="Pielęgnacja sierści.", min_experience="Basic"), "available"),
    (KOCIE_SERCE, "pracownik2@demo.pl", dict(
        name="Kłębek", species="Cat", sex="Female", breed="", size="Small",
        age_min_months=3, age_max_months=4, temperament="figlarny",
        description="Kociak znaleziony w ogrodzie. Bawi się wszystkim, co się rusza.",
        daily_needs="Karma dla kociąt, kuweta, zabawki."),
     _req("Yes", "Unknown", "Yes", "No", activity_level="High", min_experience="None"), "available"),
    (KOCIE_SERCE, "pracownik2@demo.pl", dict(
        name="Filemon", species="Cat", sex="Male", breed="Syjamski", size="Medium",
        age_min_months=24, age_max_months=36, temperament="gadatliwy",
        description="Syjamczyk z dużym zasobem słownictwa.",
        daily_needs="Karma mokra, dużo uwagi."),
     _req("Unknown", "No", "Unknown", "No", min_experience="Basic"), "stale"),
]