# Instrukcja wdrożeniowa i eksploatacyjna

## 1. Informacje ogólne

Niniejszy dokument zawiera szczegółowy opis procedury instalacji, weryfikacji i rozwiązywania problemów eksploatacyjnych dla aplikacji analizy inflacji w Polsce. Instrukcja dedykowana jest dla administratorów oraz osób oceniających projekt w celu prawidłowego uruchomienia środowiska i weryfikacji wszystkich funkcjonalności.

---

## 2. Architektura środowiska uruchomieniowego

Podczas pierwszego uruchomienia aplikacji w systemie operacyjnym automatycznie generowane są komponenty niezbędne do jej działania, które nie są wersjonowane w repozytorium Git (znajdują się w pliku `.gitignore`):

1.  **Środowisko wirtualne (.venv)**: izolowany katalog zawierający lokalną kopię interpretera Pythona oraz wszystkie biblioteki wymienione w pliku `requirements.txt`. Zapobiega to konfliktom wersji bibliotek w systemie operacyjnym.
2.  **Baza danych SQLite (users.db)**: lokalny plik relacyjnej bazy danych. Jeśli plik nie istnieje, system automatycznie tworzy strukturę tabel oraz domyślne konto administratora (`admin`).
3.  **Katalogi pamięci podręcznej (__pycache__)**: katalogi generowane przez interpreter Pythona, przechowujące skompilowany kod bajtowy (`.pyc`), co przyspiesza kolejne uruchomienia aplikacji.

---

## 3. Szczegółowa procedura uruchomienia

### 3.1. Uruchomienie automatyczne (system Windows)
Najprostszą i zalecaną metodą wdrożenia w systemie Windows jest użycie pliku `URUCHOM.bat`. Plik ten wykonuje kolejno następujące operacje w interpreterze poleceń Windows Command Prompt:
1.  Ustawienie kodowania znaków w konsoli na UTF-8 (`chcp 65001`) w celu poprawnego wyświetlania komunikatów z polskimi znakami.
2.  Przejście do katalogu roboczego projektu.
3.  Wyszukanie systemowego interpretera Pythona za pomocą poleceń systemowych (`py` lub `python`). W przypadku braku interpretera wyświetlany jest czytelny komunikat błędu z linkiem do pobrania środowiska.
4.  Weryfikacja istnienia katalogu `.venv`. Jeśli go nie ma, skrypt wywołuje polecenie `%SYSTEM_PYTHON% -m venv .venv`.
5.  Weryfikacja poprawności instalacji bibliotek. Jeśli jakiejkolwiek biblioteki brakuje, instaluje je za pomocą polecenia `pip install -r requirements.txt`.
6.  Wywołanie asynchronicznego skryptu w tle (PowerShell), który odczekuje 2 sekundy i otwiera przeglądarkę internetową pod adresem http://127.0.0.1:5000.
7.  Uruchomienie serwera Flask komendą `python app.py`.

### 3.2. Uruchomienie ręczne (dowolny system operacyjny)
W celu ręcznego uruchomienia w terminalu systemowym należy przejść do katalogu głównego projektu i wykonać sekwencję komend:

```bash
# Krok 1: Utworzenie srodowiska wirtualnego
python -m venv .venv

# Krok 2: Aktywacja srodowiska
# W systemie Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# W systemie Windows (CMD):
.\.venv\Scripts\activate.bat
# W systemach Unix / macOS:
source .venv/bin/activate

# Krok 3: Instalacja zaleznosci
pip install -r requirements.txt

# Krok 4: Uruchomienie aplikacji
python app.py
```

---

## 4. Konfiguracja zaawansowana

Aplikacja umożliwia zmianę domyślnych parametrów działania przy użyciu zmiennych środowiskowych systemu operacyjnego. Zmienne te muszą zostać ustawione przed wykonaniem skryptu uruchomieniowego:

*   **Zmiana domyślnego hasła administratora**:
    Domyślne hasło konta `admin` to `admin123`. Aby ustawić inne hasło przed pierwszym utworzeniem bazy danych (czyli przed wygenerowaniem pliku `users.db`), należy wywołać w PowerShell:
    ```powershell
    $env:DEFAULT_ADMIN_PASSWORD="WłasneNoweHasło"
    python app.py
    ```
    *Uwaga*: Jeśli plik `users.db` już istnieje, zmiana tej zmiennej nie wpłynie na istniejące konto. Należy najpierw usunąć plik bazy danych `users.db`, co wymusi jej ponowną inicjalizację.

*   **Ustawienie klucza sesji (SECRET_KEY)**:
    Do kryptograficznego podpisywania ciasteczek sesyjnych Flask używa klucza. Można go nadpisać za pomocą:
    ```powershell
    $env:SECRET_KEY="BardzoDlugiLosowyKompaktowyCigZnakowSzyfrujacych"
    python app.py
    ```

*   **Uruchomienie w trybie debugowania**:
    Domyślnie tryb debugowania jest wyłączony. Aby go włączyć (co pozwala na podgląd błędów w przeglądarce oraz automatyczne przeładowywanie serwera po modyfikacji kodu), należy wywołać:
    ```powershell
    $env:FLASK_DEBUG="1"
    python app.py
    ```

---

## 5. Dane źródłowe i ich integralność

Aplikacja opiera się na pliku danych GUS zlokalizowanym pod ścieżką:
`data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv`

W celu zapewnienia wysokiej spójności danych, plik ten nie może być modyfikowany, przenoszony ani dzielony. Projekt eliminuje redundancję (powielanie) danych — w repozytorium znajduje się wyłącznie jeden plik CSV zawierający pełną serię czasową. Szczegóły dotyczące struktury pliku, kodowania i sposobu obliczania wskaźników opisano w dokumencie [docs/ZRODLO_DANYCH.md](ZRODLO_DANYCH.md).

---

## 6. Procedura weryfikacji poprawności działania aplikacji (Testy manualne)

W celu potwierdzenia, że aplikacja spełnia wszystkie wymagania funkcjonalne i kryteria bezpieczeństwa, należy wykonać następujące kroki testowe:

1.  **Test braku autoryzacji (Zabezpieczenie zasobów)**:
    *   Spróbuj wejść bezpośrednio na adres http://127.0.0.1:5000/dashboard przy użyciu czystej przeglądarki (lub w trybie prywatnym).
    *   *Oczekiwany rezultat*: Aplikacja odmawia dostępu, wyświetla komunikat o konieczności zalogowania i przekierowuje użytkownika na stronę logowania http://127.0.0.1:5000/.
2.  **Test błędnego uwierzytelniania**:
    *   W formularzu logowania wprowadź niepoprawny login (np. `admin_test`) lub błędne hasło (np. `błędne_hasło`).
    *   *Oczekiwany rezultat*: Serwer odrzuca żądanie, nie następuje logowanie, na stronie pojawia się czerwony komunikat błędu "Nieprawidłowy login lub hasło."
3.  **Test poprawnego logowania**:
    *   Wprowadź login `admin` oraz hasło `admin123` (lub inne hasło zdefiniowane w zmiennej środowiskowej).
    *   *Oczekiwany rezultat*: Aplikacja pomyślnie uwierzytelnia użytkownika, tworzy sesję i przekierowuje go na adres http://127.0.0.1:5000/dashboard.
4.  **Weryfikacja poprawności obliczeń i wizualizacji**:
    *   Na załadowanym dashboardzie sprawdź wyświetlane statystyki.
    *   *Oczekiwany rezultat*: Najwyższa inflacja musi wynosić `14.4%` dla roku `2022`, najnowszy wynik za rok `2025` musi wynosić `3.6%`, skumulowana zmiana cen od 2014 do 2025 roku musi wynosić w przybliżeniu `55.2%`. Na stronie muszą renderować się trzy wykresy wygenerowane z matplotlib oraz tabela zawierająca dane od 2015 do 2025 roku.
5.  **Test wylogowania**:
    *   Kliknij przycisk "Wyloguj" w prawym górnym rogu nagłówka.
    *   *Oczekiwany rezultat*: Sesja zostaje usunięta, aplikacja wyświetla komunikat "Wylogowano poprawnie.", następuje przekierowanie na stronę logowania, a ponowna próba wejścia na adres `/dashboard` jest blokowana.

---

## 7. Rozwiązywanie problemów (Troubleshooting)

### 7.1. Polecenie `python` lub `py` nie jest rozpoznawane
*   *Przyczyna*: Interpreter Pythona nie został zainstalowany w systemie operacyjnym lub jego ścieżka nie została dodana do zmiennej środowiskowej systemowej `PATH`.
*   *Rozwiązanie*: Należy pobrać instalator ze strony https://www.python.org/ i uruchomić go ponownie. W pierwszym oknie instalatora konieczne jest zaznaczenie opcji **"Add Python to PATH"** (Dodaj Pythona do zmiennej PATH).

### 7.2. Port 5000 jest zajęty (Błąd uruchomienia serwera)
*   *Przyczyna*: Inny proces w systemie operacyjnym (np. inna instancja aplikacji, serwer deweloperski, usługi systemowe macOS lub Windows) korzysta z portu sieciowego 5000.
*   *Rozwiązanie*: Należy zamknąć procesy korzystające z tego portu. W systemie Windows można zidentyfikować proces w terminalu PowerShell za pomocą komendy:
    ```powershell
    Get-NetTCPConnection -LocalPort 5000
    ```
    Po uzyskaniu identyfikatora procesu (PID) można go zakończyć w Menedżerze Zadań lub komendą `Stop-Process -Id PID`.

### 7.3. Brak zmian po modyfikacji domyślnego hasła administratora
*   *Przyczyna*: Zmienna środowiskowa `DEFAULT_ADMIN_PASSWORD` została ustawiona po tym, jak plik bazy danych `users.db` został już utworzony. Aplikacja nie nadpisuje haseł w istniejącej bazie przy każdym uruchomieniu.
*   *Rozwiązanie*: Usuń plik bazy danych `users.db` z katalogu głównego projektu i uruchom aplikację ponownie. Nowa baza danych zostanie zainicjalizowana z uwzględnieniem nowej wartości zmiennej środowiskowej.
