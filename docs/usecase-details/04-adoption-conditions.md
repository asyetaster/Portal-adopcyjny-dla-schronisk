# Ulubione i profil warunków — Adoption

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## AddAnimalToFavorites (C)

```text
AddAnimalToFavorites(
    animalId: AnimalId
)
```

Właściciel ulubionych z ActorContext; dodanie idempotentne.

## RemoveAnimalFromFavorites (C)

```text
RemoveAnimalFromFavorites(
    animalId: AnimalId
)
```

Właściciel z ActorContext; usunięcie idempotentne.

## ListMyFavoriteAnimals (Q)

```text
ListMyFavoriteAnimals(
    page: PageRequest = default
)
```

Zwraca również aktualny status i informację o niedostępności; nie ujawnia prywatnej karty.

## UpdateMyAdoptionConditions (C)

```text
UpdateMyAdoptionConditions(
    conditions: AdoptionConditions
)
```

Pełna zamiana odpowiedzi użytkownika. Konkretne pytania są propozycją, nie ustalonym wymaganiem z pliku.

## GetMyAdoptionConditions (Q)

```text
GetMyAdoptionConditions(
)
```

Właściciel z ActorContext.

## EvaluateAnimalCompatibility (Q)

```text
EvaluateAnimalCompatibility(
    animalId: AnimalId
)
```

Propozycja minimalna: porównuje zapisany profil użytkownika z aktualnymi wymaganiami. Bez zapisu i bez przesłanego przez klienta wyniku. Dla podglądu niezapisanego formularza można jawnie dodać conditions: AdoptionConditions|null = null.
