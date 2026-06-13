# Analiza inflacji w Polsce

To jest prosty projekt zaliczeniowy napisany w Pythonie i Flasku. Aplikacja:

1. wymaga zalogowania,
2. pobiera dane z lokalnego pliku GUS,
3. analizuje inflację w Polsce w latach 2015-2025,
4. pokazuje wyniki w tabeli i na trzech wykresach.

Pełne wyjaśnienie projektu znajduje się w
[DOKUMENTACJA.md](DOKUMENTACJA.md). Oryginalne wymagania prowadzącego są w
[projekt.pdf](projekt.pdf).

## Najprostsze uruchomienie

Ta metoda jest przeznaczona dla systemu Windows.

1. Zainstaluj Python 3.10 lub nowszy.
2. Kliknij dwa razy plik [`URUCHOM.bat`](../URUCHOM.bat).
3. Poczekaj, aż skrypt utworzy środowisko `.venv` i zainstaluje biblioteki.
4. Przeglądarka powinna otworzyć adres <http://127.0.0.1:5000>.
5. Zaloguj się:

```text
login: admin
hasło: admin123
```

Przy kolejnych uruchomieniach instalacja bibliotek nie jest powtarzana.
Aplikację zatrzymuje się skrótem `Ctrl+C` w oknie terminala.

## Uruchomienie ręczne

W PowerShell, w głównym katalogu projektu, wykonaj:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Następnie otwórz <http://127.0.0.1:5000>.

Jeżeli PowerShell blokuje aktywowanie środowiska, nie trzeba zmieniać polityki
systemu. Można użyć bezpośrednio:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Co powstaje przy pierwszym uruchomieniu

Aplikacja automatycznie tworzy plik `users.db`. Jest to lokalna baza SQLite z
tabelą użytkowników i kontem `admin`.

Hasło nie jest zapisane w bazie jako zwykły tekst. Zapisywany jest jego hash,
czyli wynik jednokierunkowego przekształcenia wykonywanego przez Werkzeug.

Plik `users.db` jest wpisany do `.gitignore`, dlatego nie trafia do repozytorium.
Usunięcie tego pliku powoduje utworzenie nowej bazy przy kolejnym starcie.

## Zmiana hasła początkowego

Zmiennej `DEFAULT_ADMIN_PASSWORD` trzeba użyć przed pierwszym utworzeniem bazy:

```powershell
$env:DEFAULT_ADMIN_PASSWORD="moje-nowe-haslo"
python app.py
```

Jeżeli `users.db` już istnieje, usuń go tylko wtedy, gdy świadomie chcesz
utworzyć bazę od nowa.

Można również ustawić własny klucz sesji:

```powershell
$env:SECRET_KEY="dlugi-losowy-sekretny-klucz"
python app.py
```

## Skąd pochodzą dane

Aplikacja korzysta wyłącznie z pliku:

[`data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv`](../data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv)

Jest to tabela rocznych wskaźników cen towarów i usług konsumpcyjnych dla Polski
od 1950 do 2025 roku. Źródłem danych jest Główny Urząd Statystyczny:

<https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/>

Projekt nie zawiera drugiego, ręcznie skróconego pliku z tymi samymi danymi.
Dzięki temu istnieje jedno źródło prawdy.

## Jak rozumieć wskaźnik

GUS podaje wartości przy podstawie `rok poprzedni = 100`.

- `103,6` oznacza wzrost średniego poziomu cen o `3,6%`,
- `99,1` oznacza spadek średniego poziomu cen o `0,9%`,
- `100,0` oznacza brak zmiany.

Aplikacja liczy inflację według prostego wzoru:

```text
inflacja [%] = wskaźnik GUS - 100
```

Przykład:

```text
103,6 - 100 = 3,6%
```

Skumulowany poziom cen jest liczony przez mnożenie kolejnych wskaźników. Dla
2014 roku przyjmowana jest wartość bazowa `100`.

## Co pokazuje dashboard

Po poprawnym zalogowaniu strona `/dashboard` pokazuje:

- najnowszą wartość inflacji,
- rok z najwyższą inflacją,
- skumulowaną zmianę poziomu cen od 2014 roku,
- wykres liniowy,
- wykres słupkowy,
- wykres skumulowanego poziomu cen,
- tabelę wszystkich analizowanych lat,
- krótkie wnioski i link do źródła.

Wejście na `/dashboard` bez logowania przekierowuje do formularza logowania.

## Struktura projektu

```text
projekt_python/
|-- app.py
|-- requirements.txt
|-- URUCHOM.bat
|-- .gitignore
|-- data/
|   `-- rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv
|-- docs/
|   |-- README.md
|   |-- DOKUMENTACJA.md
|   `-- projekt.pdf
|-- static/
|   `-- style.css
`-- templates/
    |-- base.html
    |-- dashboard.html
    `-- login.html
```

## Do czego służy każdy plik

- `app.py` - uruchamia Flask, bazę, logowanie, analizę i wykresy.
- `requirements.txt` - wymienia cztery wymagane biblioteki.
- `URUCHOM.bat` - automatyzuje przygotowanie i start na Windows.
- `.gitignore` - pomija środowisko, bazę i pliki tymczasowe Pythona.
- plik CSV - jest jedynym źródłem danych statystycznych.
- `templates/base.html` - wspólny układ stron.
- `templates/login.html` - formularz logowania.
- `templates/dashboard.html` - treść analizy.
- `static/style.css` - wygląd i responsywność strony.
- `docs/README.md` - instrukcja uruchomienia i szybki opis.
- `docs/DOKUMENTACJA.md` - pełne opracowanie zgodne z wymaganiami.
- `docs/projekt.pdf` - treść zadania przekazana przez prowadzącego.

## Biblioteki

- Flask - obsługa strony internetowej i adresów URL,
- Flask-Login - sesja użytkownika i ochrona dashboardu,
- pandas - odczyt i przetwarzanie CSV,
- matplotlib - generowanie wykresów.

SQLite i `sqlite3` są częścią standardowej instalacji Pythona.

## Szybkie sprawdzenie projektu

Po zainstalowaniu zależności można sprawdzić składnię:

```powershell
python -m compileall app.py
```

Następnie uruchom aplikację i sprawdź:

1. `/dashboard` bez logowania przekierowuje do `/`,
2. błędne hasło pokazuje komunikat,
3. `admin` i `admin123` otwierają dashboard,
4. tabela ma 11 wierszy, od 2015 do 2025 roku,
5. najwyższy wynik to 14,4% w 2022 roku,
6. wylogowanie ponownie blokuje dashboard.

## Najczęstsze problemy

### Polecenie `python` nie działa

Zainstaluj Pythona z <https://www.python.org/downloads/> i podczas instalacji
zaznacz `Add Python to PATH`.

### Port 5000 jest zajęty

Zamknij poprzednie okno aplikacji. W razie potrzeby sprawdź proces:

```powershell
Get-NetTCPConnection -LocalPort 5000
```

### Logowanie nie przyjmuje nowego hasła

`DEFAULT_ADMIN_PASSWORD` działa tylko podczas tworzenia nowej bazy. Istniejąca
baza zachowuje wcześniejszy hash hasła.

### Brakuje wykresów albo danych

Sprawdź, czy nie przeniesiono pliku CSV i czy jego nazwa nie została zmieniona.
Program celowo używa jednej, dokładnie określonej ścieżki do danych.
