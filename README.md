# Analiza inflacji w Polsce

Aplikacja webowa zrealizowana w języku Python z wykorzystaniem mikro-frameworka Flask, przeznaczona do analizy i wizualizacji rzeczywistych danych statystycznych Głównego Urzędu Statystycznego (GUS) dotyczących średniorocznych wskaźników cen towarów i usług konsumpcyjnych w Polsce w latach 2015–2025.

## Spis treści
1. Charakterystyka funkcjonalna
2. Wymagania systemowe i instalacja
3. Szybkie uruchomienie
4. Ręczne uruchomienie i konfiguracja
5. Struktura katalogów projektu
6. Opis stosu technologicznego
7. Dane źródłowe
8. Autoryzacja i baza danych
9. Autor projektu

---

## 1. Charakterystyka funkcjonalna

Aplikacja realizuje następujące funkcjonalności:
*   Autoryzacja użytkowników w oparciu o sesje oraz lokalną bazę danych SQLite.
*   Zabezpieczenie przed nieautoryzowanym dostępem do panelu analitycznego (dashboardu).
*   Odczyt i weryfikacja poprawności danych z pliku CSV w formacie udostępnianym przez Główny Urząd Statystyczny.
*   Wyznaczenie średniorocznej wartości inflacji procentowej oraz skumulowanego poziomu cen odniesionego do roku bazowego 2014.
*   Wizualizacja danych w postaci trzech generowanych dynamicznie wykresów (wykres liniowy trendu inflacji, wykres słupkowy porównawczy oraz wykres powierzchniowy skumulowanego poziomu cen).
*   Prezentacja wyników analizy w tabeli interaktywnej wraz z podsumowaniem kluczowych wartości makroekonomicznych (najwyższa inflacja, najnowsza inflacja, całkowity wzrost cen).

---

## 2. Wymagania systemowe i instalacja

Do poprawnego uruchomienia aplikacji wymagane jest posiadanie zainstalowanego w systemie operacyjnym środowiska interpretatora języka Python w wersji 3.10 lub nowszej.

Aplikacja automatycznie zarządza swoimi zależnościami poprzez wbudowany mechanizm środowisk wirtualnych (.venv).

Wymagane biblioteki zewnętrzne (zdefiniowane w pliku `requirements.txt`):
*   Flask: obsługa routingu i logiki serwera WWW.
*   Flask-Login: obsługa sesji użytkowników.
*   matplotlib: generowanie wykresów statystycznych.
*   pandas: odczyt i transformacja danych CSV.

---

## 3. Szybkie uruchomienie (System Windows)

W celu ułatwienia prezentacji projektu w systemie Windows przygotowano jednokliknięciowy skrypt uruchomieniowy o nazwie `URUCHOM.bat`. 

### Procedura uruchomienia:
1.  Upewnij się, że Python jest zainstalowany i dodany do zmiennej środowiskowej PATH.
2.  Uruchom plik `URUCHOM.bat` poprzez dwukrotne kliknięcie myszą.
3.  Skrypt automatycznie zweryfikuje obecność środowiska wirtualnego, utworzy je (jeśli nie istnieje), zainstaluje wymagane zależności z pliku `requirements.txt`, uruchomi serwer aplikacyjny pod adresem http://127.0.0.1:5000 oraz otworzy ten adres w domyślnej przeglądarce internetowej.
4.  W celu autoryzacji należy wprowadzić dane domyślne:
    *   **Login**: admin
    *   **Hasło**: admin123
5.  Zatrzymanie działania serwera odbywa się poprzez naciśnięcie kombinacji klawiszy `Ctrl+C` w oknie konsoli systemowej.

---

## 4. Ręczne uruchomienie i konfiguracja

W systemach operacyjnych innych niż Windows lub w przypadku chęci ręcznego sterowania procesem uruchomieniowym w konsoli PowerShell / Bash należy wykonać następujące polecenia w katalogu głównym projektu:

```powershell
# Utworzenie srodowiska wirtualnego
python -m venv .venv

# Aktywacja srodowiska (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalacja zaleznosci
pip install -r requirements.txt

# Uruchomienie aplikacji
python app.py
```

### Zmienne środowiskowe konfiguracji:
Przed uruchomieniem aplikacji można skonfigurować parametry poprzez zmienne środowiskowe:
*   `DEFAULT_ADMIN_PASSWORD`: pozwala zdefiniować hasło administratora przy pierwszym utworzeniu bazy danych (np. `$env:DEFAULT_ADMIN_PASSWORD="nowe_haslo"`).
*   `SECRET_KEY`: pozwala nadpisać klucz szyfrujący sesję (np. `$env:SECRET_KEY="tajny_klucz"`).
*   `FLASK_DEBUG`: ustawienie wartości `1` uruchamia serwer w trybie debugowania z automatycznym przeładowaniem kodu po zmianach (np. `$env:FLASK_DEBUG="1"`).

---

## 5. Struktura katalogów projektu

Poniższa struktura przedstawia rozkład plików w repozytorium:

```
projekt_python/
├── README.md               # Skrócona instrukcja uruchomieniowa (ten plik)
├── app.py                  # Główny plik aplikacji zawierający backend Flask i analizę
├── requirements.txt        # Wykaz bibliotek zewnętrznych niezbędnych do uruchomienia
├── URUCHOM.bat             # Skrypt automatyzujący uruchamianie aplikacji w systemie Windows
├── .gitignore              # Plik konfiguracyjny narzędzia Git określający pliki ignorowane
│
├── data/                   # Katalog zawierający dane wejściowe
│   └── rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv # Plik źródłowy GUS
│
├── docs/                   # Katalog z pełną dokumentacją projektową
│   ├── README.md           # Instrukcja wdrożeniowa i diagnostyczna
│   ├── DOKUMENTACJA.md     # Pełny raport z analizy, opis architektury, kodu i bazy danych
│   ├── ZRODLO_DANYCH.md    # Specyfikacja techniczna pliku wejściowego CSV i interpretacja wskaźnika
│   ├── projekt.pdf         # Wytyczne i wymagania formalne projektu narzucone przez prowadzącego
│   └── screenshots/        # Zrzuty ekranu prezentujące interfejs graficzny aplikacji
│
├── static/                 # Katalog plików statycznych serwera
│   └── style.css           # Arkusz stylów CSS definiujący wygląd aplikacji i responsywność
│
└── templates/              # Szablony HTML renderowane przez silnik Jinja2
    ├── base.html           # Szablon bazowy zawierający wspólne elementy układu (header, footer)
    ├── login.html          # Szablon formularza logowania
    └── dashboard.html      # Szablon panelu analitycznego wyświetlającego wyniki
```

---

## 6. Opis stosu technologicznego

*   **Python**: język programowania stanowiący rdzeń logiczny projektu.
*   **Flask**: mikro-framework obsługujący routing, zapytania HTTP i zarządzanie kontekstem aplikacji.
*   **Flask-Login**: bezpieczny moduł autoryzacji użytkowników na poziomie sesji.
*   **SQLite**: relacyjny silnik bazy danych zapisujący dane w pliku lokalnym.
*   **pandas**: biblioteka analityczna użyta do przetwarzania danych statystycznych.
*   **matplotlib**: biblioteka rysująca wykresy prezentowane na dashboardzie.
*   **Werkzeug**: system dostarczający funkcje haszujące hasła.

---

## 7. Dane źródłowe

Dane statystyczne wykorzystywane w projekcie pochodzą z oficjalnych zbiorów Głównego Urzędu Statystycznego (GUS). Repozytorium korzysta z jednego pliku danych obejmującego lata 1950–2025. Aplikacja filtruje ten plik programowo, co gwarantuje spójność danych i eliminuje ryzyko powstawania rozbieżności przy modyfikacji plików. Szczegółowe metadane pliku oraz instrukcja interpretacji matematycznej wskaźników GUS znajdują się w dokumencie `docs/ZRODLO_DANYCH.md`.

---

## 8. Autoryzacja i baza danych

Aplikacja przechowuje dane kont użytkowników w pliku bazy danych SQLite o nazwie `users.db`. Baza ta jest tworzona automatycznie przy pierwszym uruchomieniu programu. Hasła użytkowników są zabezpieczone przed nieautoryzowanym odczytem przy użyciu algorytmu PBKDF2 z solą kryptograficzną. Szczegółowe informacje dotyczące architektury bazy danych, schematu tabel oraz procesu uwierzytelniania zostały opisane w dokumencie `docs/DOKUMENTACJA.md`.

---

## 9. Autor projektu

Projekt został wykonany samodzielnie jako praca zaliczeniowa z przedmiotu Języki Obiektowe I (Python).

**Autor**: Jakub Liszewski  
**Uczelnia**: WSB w Chorzowie  
**Prowadzący**: mgr inż. Arkadiusz Banasik  
**Rok akademicki**: 2021/2022 (semestr letni)
