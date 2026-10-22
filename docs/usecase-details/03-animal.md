# Karty zwierząt — Animal

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## CreateAnimalProfile (C)

```text
CreateAnimalProfile(
    shelterId: ShelterId,
    name: NonEmptyString,
    species: AnimalSpecies
)
```

Minimalny szkic. Pozostałe dane przez UpdateAnimalProfile; kompletność weryfikowana przed publikacją.

## UpdateAnimalProfile (C)

```text
UpdateAnimalProfile(
    animalId: AnimalId,
    profile: AnimalProfilePatch
)
```

Bez dowolnego ustawiania statusu publikacji lub adopcji.

## UpdateAnimalCareRequirements (C)

```text
UpdateAnimalCareRequirements(
    animalId: AnimalId,
    requirements: AnimalCareRequirements
)
```

Pełna zamiana uporządkowanego zestawu wymagań; źródło dla dopasowania.

## AddAnimalPhoto (C)

```text
AddAnimalPhoto(
    animalId: AnimalId,
    upload: UploadedImage,
    altText: string
)
```

null = null|UploadedImage jest neutralnym obiektem aplikacyjnym, nie UploadedFile Symfony. Backend weryfikuje format i rozmiar; generuje photoId i klucz magazynu.

## RemoveAnimalPhoto (C)

```text
RemoveAnimalPhoto(
    animalId: AnimalId,
    photoId: AnimalPhotoId
)
```

Sprawdź przynależność zdjęcia i minimalną liczbę zdjęć opublikowanej karty.

## PublishAnimalProfile (C)

```text
PublishAnimalProfile(
    animalId: AnimalId
)
```

Kompletność, aktywność schroniska i dozwolony stan sprawdza backend.

## WithdrawAnimalProfile (C)

```text
WithdrawAnimalProfile(
    animalId: AnimalId,
    reason: NonEmptyString
)
```

Powód wymagany jako proponowana reguła audytu.

## HideAnimalProfile (C)

```text
HideAnimalProfile(
    animalId: AnimalId,
    reason: NonEmptyString
)
```

Administracyjne ukrycie, nie wycofanie przez schronisko.

## ConfirmAnimalProfileAccuracy (C)

```text
ConfirmAnimalProfileAccuracy(
    animalId: AnimalId
)
```

Czas potwierdzenia z Clock, nie z klienta.

## SearchAnimals (Q)

```text
SearchAnimals(
    filters: AnimalSearchFilters = {},
    page: PageRequest = default,
    sort: AnimalSort = Newest
)
```

Wyłącznie publiczne karty; status dostępności ograniczony do stanów widocznych publicznie.

## GetAnimalProfile (Q)

```text
GetAnimalProfile(
    animalId: AnimalId
)
```

Publiczne dane.

## GetAnimalProfileForManagement (Q)

```text
GetAnimalProfileForManagement(
    animalId: AnimalId
)
```

Odczyt zarządczy po sprawdzeniu uprawnień.

## ListShelterAnimals (Q)

```text
ListShelterAnimals(
    shelterId: ShelterId,
    filters: ShelterAnimalFilters = {},
    page: PageRequest = default,
    sort: AnimalManagementSort = UpdatedAtDesc
)
```

Odczyt zarządczy, także szkice i zakończone karty.
