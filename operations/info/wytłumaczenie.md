Co to w ogóle jest operations/
  
  To warstwa, która trzyma całą logikę operacji na danych. Każda operacja to osobna klasa, która dostaje w konstruktorze połączenie z bazą i ma jedną metodę execute() wykonującą konkretne SQL. Dzielą się na dwa rodzaje:
  
  - Command (komenda) — coś zmienia w bazie: dodaje, edytuje, usuwa.
  - Query (zapytanie) — tylko czyta z bazy, nic nie zmienia.
  
  Dzięki temu route'y w routes/ nie piszą SQL bezpośrednio, tylko wołają te klasy. Łatwiej to potem testować i utrzymać w porządku.
  
  Pliki w operations/user/
  
  - __init__.py — definiuje jedną stałą MAX_NAME_LENGTH = 100 (maksymalna długość nazwy użytkownika). Po to, żeby limit był w jednym miejscu, a nie rozsiany po kodzie.
  - CreateUserCommand.py — tworzy nowego użytkownika. Wykonuje INSERT INTO users, zwraca nowe id. Po co: gdy ktoś się rejestruje / dodaje usera w panelu.
  - GetUserQuery.py — pobiera jednego użytkownika po id. Wykonuje SELECT, zwraca słownik {id, name} albo None, jeśli nie ma takiego usera. Po co: pokazanie szczegółów usera.
  - ListUsersQuery.py — pobiera listę użytkowników ze stronicowaniem. Bierze limit i page, liczy offset i zwraca listę słowników. Po co: lista w panelu admina, gdy userów jest dużo.
  - UpdateUserCommand.py — zmienia nazwę użytkownika po id. Wykonuje UPDATE, zwraca ile wierszy zmieniono. Po co: edycja usera.
  
  Pozostałe
  
  - operations/__init__.py — pusty, tylko po to, żeby Python traktował operations jako pakiet (importowalny).
  - operations/info/wytłumaczenie.md — tu jest jakieś dodatkowe wyjaśnienie tekstowe (nie czytałem go, bo chciałeś napisane na czacie).
  
  W skrócie: to folder z „akcjami na użytkownikach". Komendy piszą do bazy, zapytania z niej czytają, a route'y tylko je wywołują.