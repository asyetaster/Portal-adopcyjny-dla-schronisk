# Operacje uruchamiane przez system

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## SendAnimalProfileAccuracyReminders (C)

```text
SendAnimalProfileAccuracyReminders(
)
```

Systemowy ActorContext. Clock, progi nieaktualności, limit częstotliwości i rozmiar partii z konfiguracji/portów. Wylicza adresatów i wysyła zbiorcze przypomnienia per placówka; backend zapewnia deduplikację. Nie wymaga przekazywania dzisiejszej daty ani listy odbiorców przez scheduler.
