Co to w ogóle jest routes/
  
  To warstwa, która odbiera żądania HTTP (adresy URL) i decyduje, co z nimi zrobić. Każdy plik definiuje funkcję register(app), która „podpina" dane endpointy pod aplikację Flask. Wewnątrz route woła operacje z operations/
  (czyli nie pisze SQL sam) i zwraca dane do szablonu HTML.
  
  Warto zauważyć: endpointy nie renderują szablonu ręcznie. Mają dekorator @page("ścieżka/szablonu.html"), który sam zajmuje się wyświetleniem. Dodatkowo obiekty z operations (np. CreateUserCommand) są wstrzykiwane jako
  parametry funkcji — Flask dostaje je automatycznie, route ich nie tworzy sam.
  
  Pliki w routes/
  
  - routes/__init__.py — automatyczne wykrywanie tras. Przechodzi po wszystkich modułach w pakiecie i woła ich register(app), jeśli taki znajdzie. Dzięki temu dodanie nowego pliku z trasą nie wymaga edycji app.py — wystarczy
  dorzucić plik i działa. Korzysta z pomocniczego discovery.py.
  - routes/user/__init__.py — współdzielone helpery dla tras userów. Definiuje read_user_name(field): czyta nazwę z formularza, sprawdza że nie jest pusta i nie przekracza MAX_NAME_LENGTH, a przy błędzie przerywa z 400. Po co,
  żeby walidacja nazwy była w jednym miejscu, a nie powielana w każdym route.
  
  Pliki w routes/user/
  
  - create.py — dodawanie użytkownika (POST /admin/users). Czyta nazwę z formularza, woła CreateUserCommand, pokazuje komunikat „Utworzono użytkownika" i przekierowuje na stronę szczegółów nowego usera. Po co: formularz „nowy
  użytkownik" w panelu.
  - details.py — szczegóły użytkownika (GET /admin/users/<id>). Woła GetUserQuery, a jak usera nie ma, zwraca 404. Po co: podgląd jednego usera.
  - list.py — lista użytkowników (GET /admin/users). Woła ListUsersQuery i zwraca listę do szablonu. Po co: tabela userów w panelu admina.
  - update.py — zmiana nazwy użytkownika (POST /admin/users/<id>). Sprawdza czy user istnieje, woła UpdateUserCommand, pokazuje komunikat potwierdzający. Po co: edycja usera.
  
  Podsumowanie
  
  W routes leżą endpointy (adresy). Każdy route przyjmuje żądanie, waliduje dane, woła odpowiednią operację z operations/ i oddaje wynik do szablonu. Taka separacja: route odpowiada za „co robimy z tym żądaniem", operacja
  odpowiada za „co robimy z bazą".