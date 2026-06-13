# Dokumentacja projektu

## 1. Informacje podstawowe

**Nazwa projektu:** Analiza inflacji w Polsce w latach 2015-2025

**Przedmiot:** Języki Obiektowe I (Python)

**Autor i zakres pracy:** Jakub Liszewski - wybór danych, analiza, backend,
logowanie, baza danych, frontend, testy i dokumentacja.

Projekt został przygotowany jako projekt jednoosobowy. Wymaganie z pliku
`projekt.pdf` dopuszcza zespoły maksymalnie trzyosobowe, ale nie wymaga, aby
zespół miał trzy osoby [6].

## 2. Temat projektu

Tematem jest analiza rzeczywistych danych statystycznych dostępnych online oraz
przedstawienie wyników na stronie internetowej. Wybrano średnioroczne wskaźniki
cen towarów i usług konsumpcyjnych w Polsce, potocznie nazywane inflacją.

Analiza obejmuje lata 2015-2025. Dane pochodzą z oficjalnej tabeli Głównego
Urzędu Statystycznego [1]. Aplikacja używa lokalnej kopii tej tabeli, dlatego po
zainstalowaniu bibliotek działa również bez połączenia z internetem.

## 3. Cel projektu

Głównym celem było zbudowanie małej, kompletnej aplikacji, która:

1. korzysta z prawdziwych danych statystycznych,
2. wykonuje na nich zrozumiałą analizę,
3. przedstawia wyniki na stronie internetowej,
4. wymaga zalogowania do konta przechowywanego w bazie danych,
5. jest łatwa do uruchomienia i zaprezentowania.

Cel został osiągnięty. Użytkownik niezalogowany widzi formularz logowania.
Użytkownik zalogowany widzi dashboard z wartościami, trzema wykresami, tabelą i
wnioskami.

## 4. Co oznaczają analizowane dane

GUS publikuje wskaźnik przy podstawie:

```text
rok poprzedni = 100
```

Liczba `100` jest punktem odniesienia:

- wynik większy od 100 oznacza wzrost cen,
- wynik mniejszy od 100 oznacza spadek cen,
- wynik równy 100 oznacza brak średniej zmiany cen.

Przykłady:

```text
wskaźnik 103,6 -> ceny wzrosły średnio o 3,6%
wskaźnik 99,1  -> ceny spadły średnio o 0,9%
wskaźnik 100,0 -> średni poziom cen się nie zmienił
```

GUS potwierdza, że średnioroczny wskaźnik w 2025 roku wyniósł `103,6`, czyli
średni wzrost cen wyniósł `3,6%` [2].

## 5. Jedno źródło danych

Projekt korzysta wyłącznie z pliku:

```text
data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv
```

Plik zawiera 76 wierszy danych, od 1950 do 2025 roku. Aplikacja wybiera z niego
11 wierszy, od 2015 do 2025 roku.

Nie istnieje drugi, ręcznie przygotowany plik z wybranymi latami. Usunięcie
duplikatu jest ważne, ponieważ dwa pliki z tymi samymi liczbami mogłyby z czasem
zacząć się różnić. Jeden plik oznacza jedno źródło prawdy.

Format pliku GUS:

- separator kolumn: średnik `;`,
- separator dziesiętny: przecinek `,`,
- kodowanie znaków: Windows-1250,
- najważniejsze kolumny: `Rok` i `Wartość`.

Te informacje są jawnie podane w funkcji `load_inflation_data()` w `app.py`.

## 6. Jak przebiega analiza

### Krok 1: odczyt pliku

Pandas odczytuje pełny plik:

```python
pd.read_csv(DATA_PATH, sep=";", decimal=",", encoding="cp1250")
```

Każdy parametr ma znaczenie:

- `DATA_PATH` wskazuje plik,
- `sep=";"` rozdziela kolumny,
- `decimal=","` zamienia polski zapis dziesiętny na liczby,
- `encoding="cp1250"` poprawnie odczytuje polskie znaki.

### Krok 2: kontrola kolumn

Program sprawdza, czy istnieją kolumny `Rok` i `Wartość`. Bez nich dalsza
analiza nie miałaby sensu, więc zgłaszany jest czytelny błąd.

### Krok 3: wybór lat

Z pełnej tabeli wybierane są lata od 2015 do 2025. Kolumny otrzymują prostsze
nazwy używane w kodzie:

```text
Rok     -> rok
Wartość -> wskaznik_cen
```

Program sprawdza również, czy każdy oczekiwany rok występuje dokładnie raz.
Chroni to analizę przed brakującym lub powtórzonym wierszem.

### Krok 4: obliczenie inflacji

Inflacja procentowa jest obliczana tak:

```text
inflacja_proc = wskaznik_cen - 100
```

Dla 2025 roku:

```text
103,6 - 100 = 3,6%
```

### Krok 5: obliczenie skumulowanego poziomu cen

Rok 2014 jest punktem bazowym równym 100. Każdy kolejny wskaźnik jest zamieniany
na mnożnik i mnożony przez wynik z poprzednich lat:

```text
poziom_cen = iloczyn(wskaznik_cen / 100) * 100
```

Nie wolno dodawać rocznych inflacji, ponieważ kolejne zmiany procentowe działają
na coraz innym poziomie cen. Dlatego używany jest iloczyn, a nie suma.

Wynik dla końca badanego okresu to około `155,23`. Oznacza to, że średni poziom
cen był w 2025 roku o około `55,23%` wyższy niż w 2014 roku.

## 7. Wyniki analizy

Najważniejsze wyniki obliczone z dołączonego pliku GUS:

| Rok | Wskaźnik GUS | Inflacja |
|---:|---:|---:|
| 2015 | 99,1 | -0,9% |
| 2016 | 99,4 | -0,6% |
| 2017 | 102,0 | 2,0% |
| 2018 | 101,6 | 1,6% |
| 2019 | 102,3 | 2,3% |
| 2020 | 103,4 | 3,4% |
| 2021 | 105,1 | 5,1% |
| 2022 | 114,4 | 14,4% |
| 2023 | 111,4 | 11,4% |
| 2024 | 103,6 | 3,6% |
| 2025 | 103,6 | 3,6% |

Wnioski:

1. Najwyższa średnioroczna inflacja wystąpiła w 2022 roku i wyniosła 14,4%.
2. W 2015 i 2016 roku wystąpiła niewielka deflacja.
3. W 2023 roku inflacja nadal była wysoka i wyniosła 11,4%.
4. W 2024 i 2025 roku tempo wzrostu cen spadło do 3,6%.
5. Spadek inflacji nie oznacza powrotu cen do wcześniejszego poziomu.
6. Skumulowany wzrost poziomu cen od 2014 do 2025 roku wyniósł około 55,23%.

Wartość dla 2025 roku jest zgodna z osobnym komunikatem GUS [2].

## 8. Jak działa aplikacja internetowa

### Uruchomienie

Python wykonuje plik `app.py`. Flask uruchamia lokalny serwer pod adresem:

```text
http://127.0.0.1:5000
```

Jest to adres lokalny. Strona nie jest automatycznie publikowana w internecie.

### Baza danych

Funkcja `init_db()` tworzy plik `users.db` i tabelę:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
```

Znaczenie pól:

- `id` - numer użytkownika,
- `username` - unikalny login,
- `password_hash` - hash hasła.

Jeżeli konto `admin` nie istnieje, program je tworzy. Domyślne hasło to
`admin123`, ale może zostać zmienione zmienną `DEFAULT_ADMIN_PASSWORD` przed
pierwszym uruchomieniem.

### Dlaczego hasło nie jest zapisane jawnie

Funkcja `generate_password_hash()` tworzy hash. Podczas logowania funkcja
`check_password_hash()` porównuje wpisane hasło z hashem. Aplikacja nie musi
przechowywać zwykłego tekstu hasła.

To jest poprawniejszy sposób niż zapisanie `admin123` bezpośrednio w bazie.
Projekt jest jednak aplikacją demonstracyjną, a nie gotowym systemem
produkcyjnym.

### Logowanie

Adres `/` obsługuje formularz:

1. użytkownik wpisuje login i hasło,
2. aplikacja szuka loginu w SQLite,
3. aplikacja sprawdza hash hasła,
4. po sukcesie Flask-Login zapisuje użytkownika w sesji,
5. następuje przekierowanie do `/dashboard`.

Błędne dane nie otwierają analizy i powodują wyświetlenie komunikatu.

### Ochrona analizy

Widok dashboardu ma dekorator:

```python
@login_required
```

To oznacza, że niezalogowana osoba nie może bezpośrednio otworzyć analizy.
Flask-Login przekieruje ją do formularza logowania.

Spełnia to wymaganie z `projekt.pdf`: treść analizy jest dostępna po zalogowaniu
do konta użytkownika przechowywanego w bazie [6].

### Wylogowanie

Przycisk wysyła żądanie `POST` do `/logout`. Funkcja `logout_user()` usuwa dane
logowania z sesji. Po wylogowaniu dashboard jest ponownie zablokowany.

## 9. Wykresy

Matplotlib generuje trzy wykresy:

1. liniowy wykres inflacji,
2. słupkowe porównanie lat,
3. skumulowany poziom cen przy podstawie `2014 = 100`.

Wykresy nie są zapisywane jako pliki na dysku. Powstają w pamięci jako PNG,
są kodowane do Base64 i umieszczane bezpośrednio w HTML.

Zalety:

- brak katalogu z generowanymi obrazami,
- brak sprzątania starych plików,
- każdy wykres odpowiada aktualnie wczytanym danym.

## 10. Frontend

Warstwa widoczna dla użytkownika składa się z:

- HTML,
- szablonów Jinja2 dostarczanych przez Flask,
- jednego pliku CSS,
- obrazów wykresów wygenerowanych przez Matplotlib.

`base.html` zawiera wspólny nagłówek, komunikaty i stopkę. `login.html` zawiera
formularz. `dashboard.html` zawiera analizę. `style.css` odpowiada za kolory,
układ kart, tabelę i dostosowanie strony do małych ekranów.

Projekt nie wymaga JavaScriptu ani zewnętrznego frameworka CSS.

## 11. Stos technologiczny

| Technologia | Zastosowanie |
|---|---|
| Python | główny język |
| Flask | serwer WWW, routing i szablony |
| Flask-Login | logowanie, sesja i ochrona widoków |
| SQLite | lokalna baza użytkowników |
| pandas | odczyt i analiza CSV |
| Matplotlib | wykresy |
| Werkzeug | hashowanie i sprawdzanie haseł |
| HTML i Jinja2 | budowa stron |
| CSS | wygląd i responsywność |
| Git i GitHub | wersjonowanie projektu |

Flask opisuje sposób tworzenia tras i renderowania szablonów w oficjalnej
dokumentacji [3]. Flask-Login dokumentuje `login_user`, `logout_user` i
`login_required` [4]. Pandas opisuje funkcję `read_csv` [5].

## 12. Struktura i odpowiedzialność plików

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

W projekcie nie ma zbędnego skróconego CSV, zapisanych wykresów ani bazy
użytkowników w repozytorium.

## 13. Instrukcja prezentacji projektu

Najprostsza kolejność podczas prezentacji:

1. pokaż plik źródłowy GUS w katalogu `data`,
2. uruchom `URUCHOM.bat`,
3. spróbuj wejść bezpośrednio na `/dashboard`,
4. pokaż przekierowanie do logowania,
5. wpisz błędne hasło i pokaż komunikat,
6. zaloguj się jako `admin`,
7. omów trzy najważniejsze wartości,
8. wyjaśnij różnicę między inflacją a poziomem cen,
9. pokaż tabelę i trzy wykresy,
10. wyloguj się i pokaż, że dashboard znów jest chroniony.

## 14. Weryfikacja wymagań z projekt.pdf

| Wymaganie | Sposób spełnienia | Status |
|---|---|---|
| Skład zespołu i role | Podane w sekcji 1 | Spełnione |
| Opis tematyki | Sekcje 2 i 4 | Spełnione |
| Cel projektu | Sekcja 3 | Spełnione |
| Opis realizacji i osiągnięcia celu | Sekcje 5-10 | Spełnione |
| Zadania, technologie i realizacja | Sekcje 5, 6, 8-12 | Spełnione |
| Wnioski i dalszy rozwój | Sekcje 7 i 15 | Spełnione |
| Bibliografia i cytowania | Cytowania [1]-[6], sekcja 16 | Spełnione |
| Rzeczywiste dane online | Oficjalne dane GUS [1] i lokalny CSV | Spełnione |
| Strona internetowa we Flasku | `app.py` i szablony | Spełnione |
| Logowanie oparte o bazę | SQLite, tabela `users`, Flask-Login | Spełnione |
| Analiza po zalogowaniu | `@login_required` na `/dashboard` | Spełnione |
| Indywidualna wizualizacja | CSS, karty, tabela i trzy wykresy | Spełnione |
| Dokumentacja dołączona do projektu | Ten plik i README w `docs` | Spełnione |

Wymaganie zatwierdzenia tematu przez prowadzącego oraz prezentacji na forum
grupy jest organizacyjne. Nie da się go potwierdzić samym kodem ani historią
Git. Musi zostać wykonane przez autora poza repozytorium.

Podobnie wysłanie plików na PZE jest czynnością wykonywaną poza projektem.
Repozytorium zawiera komplet plików, które można przesłać.

## 15. Możliwości dalszego rozwoju

Obecna wersja spełnia wymagania projektu. Możliwe rozszerzenia:

- rejestracja nowych użytkowników,
- formularz zmiany hasła,
- automatyczne pobieranie nowego pliku GUS,
- wybór zakresu lat przez użytkownika,
- analiza danych miesięcznych,
- porównanie inflacji z wynagrodzeniami,
- eksport wykresów lub raportu,
- testy automatyczne uruchamiane na GitHub Actions,
- wdrożenie aplikacji na serwerze.

Rozszerzenia nie są potrzebne do spełnienia wymagań z `projekt.pdf`.

## 16. Bibliografia

[1] Główny Urząd Statystyczny, „Roczne wskaźniki cen towarów i usług
konsumpcyjnych od 1950 r.”,
<https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/>,
dostęp: 13.06.2026.

[2] Główny Urząd Statystyczny, „Komunikat w sprawie średniorocznego wskaźnika
cen towarów i usług konsumpcyjnych ogółem w 2025 r.”,
<https://stat.gov.pl/sygnalne/komunikaty-i-obwieszczenia/lista-komunikatow-i-obwieszczen/komunikat-w-sprawie-sredniorocznego-wskaznika-cen-towarow-i-uslug-konsumpcyjnych-ogolem-w-2025-r-%2C50%2C13.html>,
dostęp: 13.06.2026.

[3] Pallets Projects, „Flask Documentation”,
<https://flask.palletsprojects.com/>, dostęp: 13.06.2026.

[4] Flask-Login, „Flask-Login Documentation”,
<https://flask-login.readthedocs.io/>, dostęp: 13.06.2026.

[5] pandas, „pandas.read_csv”,
<https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html>,
dostęp: 13.06.2026.

[6] Arkadiusz Banasik, „Języki Obiektowe I (Python) - Zajęcia 5”, WSB w
Chorzowie, 6.03.2022, plik `docs/projekt.pdf` dołączony do repozytorium.
