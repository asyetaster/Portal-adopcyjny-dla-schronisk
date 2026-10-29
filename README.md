# Portal-adopcyjny-dla-schronisk
Platforma, na której schroniska publikują zwierzęta dostępne do adopcji, a użytkownicy wyszukują podopiecznych i zgłaszają zainteresowanie.

# Instalacja Linux

## Instalacja od zera (jednorazowo)

Wymagania: Python 3.11 lub nowszy (`python3 --version`). Polecenia uruchamiaj w katalogu projektu.

```bash
python3 -m venv .venv               # środowisko wirtualne
source .venv/bin/activate           # aktywacja
pip install -r requirements.txt     # Flask, Flask-WTF, SQLAlchemy
python database.py                  # tworzy app.db z tabelą users (można uruchamiać wielokrotnie)
```

## Uruchamianie (za każdym razem)

```bash
source .venv/bin/activate
flask --app app run --debug         # hot reloading (.py i szablony) + debugger w przeglądarce
```
# Instalacja Windows

## Instalacja od zera — **Windows** (PowerShell)

Wymagania: Python 3.11 lub nowszy (`python --version`). Polecenia uruchamiaj w katalogu projektu.

```powershell
python -m venv .venv                # środowisko wirtualne
.\.venv\Scripts\Activate.ps1         # aktywacja
pip install -r requirements.txt     # Flask, Flask-WTF, SQLAlchemy
python database.py                  # tworzy app.db z tabelą users (można uruchamiać wielokrotnie)
```

## Uruchamianie (za każdym razem)

```powershell
.\.venv\Scripts\Activate.ps1
flask --app app run --debug         # hot reloading (.py i szablony) + debugger w przeglądarce
```


# LLM CRUD context generator

Dla szybszego generowania operacji CRUD przez czaty AI dostępny jest generator kontekstu,
który na podstawie CRUD użytkownika (oraz schematu bazy danych) generuje przykład wzorca naszego CRUD-a.

## Użycie Linux

```bash
./crud-context-generator.sh > tmp.txt # bez schematu bazy danych
./crud-context-generator.sh --with-database > tmp.txt # z schematem bazy danych
```

## Użycie windows
```powershell
.\crud-context-generator.ps1 > tmp.txt # bez schematu bazy danych
.\crud-context-generator.ps1 --with-database > tmp.txt # z schematem bazy danych
```

Kontekst w powyższych użyciach generuje się gotowy do skopiowania do pliku tmp.txt