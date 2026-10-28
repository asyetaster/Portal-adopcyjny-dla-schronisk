# Konta użytkowników — Identity

Proponowane parametry wejściowe na podstawie `useCases.md`. Definicje wszystkich DTO, enumów, identyfikatorów i zasad znajdują się w `00-typy-i-zalozenia.md`.

Każda operacja korzysta z zaufanego ActorContext; nie jest on polem formularza. C = command, Q = query. Parametry dodatkowe i reguły nieustalone w źródle są propozycją projektową.

## RegisterUser (C)

```text
RegisterUser(
    email: EmailAddress,
    plainPassword: string,
    firstName: NonEmptyString,
    lastName: NonEmptyString,
    phone: PhoneNumber
)
```

null = null|Publiczny. Hasło tylko na wejściu; nie trafia do logów ani zdarzeń. Wymagalność nazwiska i telefonu to założenie.

## GetMyProfile (Q)

```text
GetMyProfile(
)
```

Użytkownik wynika z ActorContext.

## UpdateMyProfile (C)

```text
UpdateMyProfile(
    profile: UserProfilePatch
)
```

PATCH; bez zmiany e-maila i hasła, bo dokument wymienia imię i kontakt, a nie zmianę danych logowania.

## BlockUser (C)

```text
BlockUser(
    userId: UserId,
    reason: NonEmptyString
)
```

Administrator; nie przyjmuj roli ani uprawnień z żądania.

## DeleteUserAccount (C)

```text
DeleteUserAccount(
)
```

Własne konto z ActorContext. Backend sprawdza aktywne adopcje, wolontariat i spacery. Ponowne uwierzytelnienie w adapterze bezpieczeństwa.

## AnonymizeUserAccount (C)

```text
AnonymizeUserAccount(
    userId: UserId,
    reason: NonEmptyString
)
```

Założenie: operacja administratora lub procesu retencji. Dla samoobsługi cel musi pochodzić z ActorContext. Zachowuje wymaganą historię transakcji, a nie dane identyfikujące.
