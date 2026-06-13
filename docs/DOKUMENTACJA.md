# Dokumentacja techniczna projektu zaliczeniowego

## 1. Skład zespołu oraz role w projekcie

Projekt został zrealizowany w formie jednoosobowej przez następującego autora:

*   **Jakub Liszewski**: odpowiedzialny za pełny cykl życia oprogramowania, w tym:
    *   pozyskanie i weryfikację poprawności danych statystycznych z Głównego Urzędu Statystycznego (GUS),
    *   zaprojektowanie i implementację warstwy backendowej w języku Python z wykorzystaniem mikro-frameworka Flask,
    *   zaprojektowanie i implementację mechanizmów bezpieczeństwa oraz sesji użytkownika (Flask-Login, Werkzeug),
    *   zaprojektowanie bazy danych SQLite oraz wdrożenie mechanizmów mapowania i haszowania haseł,
    *   przygotowanie skryptów analitycznych (biblioteka pandas) oraz modułu wizualizacji danych (biblioteka matplotlib),
    *   przygotowanie szablonów interfejsu użytkownika (HTML, Jinja2, CSS),
    *   przeprowadzenie testów funkcjonalnych systemu,
    *   stworzenie dokumentacji projektowej i technicznej.

Zgodnie z wymaganiami określonymi w dokumencie projektowym, dopuszczalny maksymalny skład sekcji wynosi trzy osoby. Samodzielna realizacja projektu w pełni spełnia kryteria formalne, zapewniając autorowi pełną kontrolę nad spójnością architektoniczną rozwiązania.

---

## 2. Opis tematyki projektu

Tematem projektu jest analiza średniorocznych wskaźników cen towarów i usług konsumpcyjnych w Polsce w okresie lat 2015–2025. Wskaźniki te, powszechnie określane mianem inflacji, stanowią jeden z najważniejszych mierników makroekonomicznych określających dynamikę zmian siły nabywczej pieniądza w gospodarce.

Dane wejściowe stanowią oficjalne, historyczne oraz prognozowane/potwierdzone odczyty publikowane przez Główny Urząd Statystyczny (GUS). Aplikacja przetwarza te dane w celu wyznaczenia:
1.  Średniorocznej wartości inflacji w ujęciu procentowym rok do roku.
2.  Porównania różnic w poziomach zmian cen w poszczególnych latach.
3.  Skumulowanego wzrostu poziomu cen w całym badanym okresie odniesionego do roku bazowego 2014.

Prezentacja wyników odbywa się w sposób graficzny oraz tabelaryczny, co umożliwia interpretację trendów makroekonomicznych zachodzących w polskiej gospodarce na przestrzeni ostatniej dekady.

---

## 3. Cel realizacji projektu

Głównym celem projektu było zaprojektowanie, zaimplementowanie i przetestowanie funkcjonalnej aplikacji internetowej, która łączy w sobie cechy systemu analizy danych (Data Science) oraz bezpiecznej aplikacji webowej.

Cele szczegółowe obejmowały:
*   Zaimplementowanie mechanizmu odczytu rzeczywistych danych z pliku w formacie CSV o strukturze narzuconej przez zewnętrzny urząd statystyczny.
*   Zapewnienie bezpieczeństwa danych poprzez ograniczenie dostępu do wyników analizy wyłącznie dla uwierzytelnionych użytkowników.
*   Zaimplementowanie trwałego przechowywania danych użytkowników w relacyjnej bazie danych SQLite.
*   Automatyczne generowanie wykresów statystycznych w locie bez konieczności zapisywania plików na dysku serwera (generowanie do strumienia pamięciowego i kodowanie do standardu Base64).
*   Stworzenie ergonomicznego, responsywnego interfejsu graficznego zgodnego z zasadami User Experience (UX) oraz Responsive Web Design (RWD).

---

## 4. Opis realizacji i sposobu osiągnięcia celu projektowego

Cel projektowy został osiągnięty poprzez podział prac na trzy główne etapy: analityczny, bazodanowo-logiczny oraz prezentacyjny.

### 4.1. Etap analityczny
W pierwszym etapie pozyskano kompletny zbiór danych GUS od 1950 roku. Zaimplementowano logikę filtrującą w bibliotece pandas, która dynamicznie ogranicza zbiór danych do lat 2015–2025. Na tym etapie wprowadzono rygorystyczne testy integralności danych: aplikacja weryfikuje istnienie wymaganych kolumn oraz sprawdza, czy zbiór danych dla wybranego zakresu lat jest ciągły i kompletny.

### 4.2. Etap bazodanowo-logiczny
Wdrożono lokalną bazę danych SQLite, która przechowuje informacje o użytkownikach uprawnionych do wyświetlania analiz. Połączenie bazy danych z aplikacją zrealizowano za pomocą wbudowanego modułu `sqlite3` oraz biblioteki `Flask-Login` odpowiedzialnej za zarządzanie sesjami użytkowników. W celu zapewnienia bezpieczeństwa wdrożono algorytm haszowania haseł PBKDF2 z solą, zapobiegający przechowywaniu haseł w formie czystego tekstu.

### 4.3. Etap prezentacyjny
Zaprojektowano strukturę szablonów HTML z wykorzystaniem silnika Jinja2. Interfejs został podzielony na stronę logowania oraz dashboard analityczny. Warstwa wizualna została opisana w arkuszu stylów CSS z użyciem nowoczesnych zmiennych CSS (Custom Properties) oraz elastycznych siatek (CSS Grid) i kontenerów (Flexbox), co zapewnia prawidłowe wyświetlanie aplikacji na urządzeniach mobilnych oraz desktopowych.

---

## 5. Opis zadań projektowych, stosu technologicznego i sposobu ich realizacji

### 5.1. Stos technologiczny
Projekt został oparty o następujące komponenty programistyczne:
*   **Python (wersja 3.10 lub nowsza)**: główny język programowania użyty do logiki aplikacji, obliczeń i komunikacji z bazą danych.
*   **Flask (wersja 3.x)**: mikro-framework webowy w języku Python, odpowiadający za routing (obsługę żądań HTTP), sesje oraz integrację z silnikiem szablonów Jinja2.
*   **Flask-Login**: rozszerzenie systemu Flask dedykowane do zarządzania sesjami użytkowników, obsługujące logowanie, wylogowanie oraz zabezpieczanie ścieżek aplikacji.
*   **pandas (wersja 2.x)**: biblioteka przeznaczona do analizy i manipulacji danymi strukturalnymi. Użyta do wczytywania, oczyszczania i transformacji pliku CSV.
*   **matplotlib (wersja 3.x)**: biblioteka do tworzenia wizualizacji danych. Odpowiada za generowanie wykresów w formacie wektorowym/rastrowym.
*   **SQLite (wbudowany w standardową bibliotekę Pythona)**: lekki, bezserwerowy, relacyjny silnik baz danych przechowujący dane w pojedynczym pliku na dysku.
*   **Werkzeug**: biblioteka dostarczająca narzędzia pomocnicze dla systemu Flask, wykorzystana do bezpiecznego szyfrowania i weryfikacji haseł.

### 5.2. Szczegółowe omówienie architektury bazy danych SQLite i mechanizmów uwierzytelniania

Zgodnie z wymaganiami projektowymi, dostęp do analizy danych jest chroniony systemem logowania opartym o bazę danych. W projekcie wykorzystano silnik **SQLite**. 

#### 5.2.1. Czym jest SQLite i baza danych w pliku
SQLite to relacyjny system zarządzania bazą danych (RDBMS), który w przeciwieństwie do systemów takich jak MySQL, PostgreSQL czy Microsoft SQL Server nie działa jako oddzielny proces sieciowy (serwer). Cała baza danych SQLite (struktura tabel, indeksy oraz same dane) jest zapisywana w jednym, zwykłym pliku na dysku. W tym projekcie plik ten nosi nazwę `users.db` i jest tworzony dynamicznie w katalogu głównym projektu podczas pierwszego uruchomienia aplikacji.

Zalety tego podejścia w projekcie akademickim to:
*   Brak konieczności instalowania i konfigurowania zewnętrznego serwera baz danych przez osobę uruchamiającą projekt.
*   Całkowita przenośność projektu — plik bazy danych można łatwo skopiować wraz z resztą kodu.
*   Szybkość działania przy operacjach jednowątkowych.

#### 5.2.2. Struktura tabeli użytkowników
Baza danych zawiera jedną tabelę o nazwie `users`. Definicja tej tabeli w języku SQL wygląda następująco:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
```

Wyjaśnienie poszczególnych elementów struktury tabeli:
*   `id`: klucz główny (PRIMARY KEY). Jest to unikalny identyfikator każdego wiersza w bazie danych. Atrybut `AUTOINCREMENT` powoduje, że przy dodawaniu każdego kolejnego użytkownika system SQLite automatycznie przypisuje mu kolejną liczbę całkowitą (1, 2, 3 itd.), eliminując potrzebę ręcznego generowania unikalnych identyfikatorów.
*   `username`: kolumna przechowująca unikalny login użytkownika. Atrybut `UNIQUE` gwarantuje, że w bazie danych nie mogą istnieć dwa konta o takim samym loginie. Atrybut `NOT NULL` oznacza, że pole to nie może być puste.
*   `password_hash`: kolumna przechowująca zaszyfrowaną postać hasła (skrót kryptograficzny). Ze względów bezpieczeństwa w bazie nie wolno przechowywać haseł w formie jawnej (np. jako napis "admin123").

#### 5.2.3. Bezpieczeństwo i haszowanie haseł
Przechowywanie haseł w postaci jawnej (czystego tekstu) w bazie danych stanowi krytyczny błąd bezpieczeństwa. W przypadku wycieku bazy danych, napastnik uzyskuje bezpośredni dostęp do kont wszystkich użytkowników. Aby temu zapobiec, zastosowano mechanizm haszowania kryptograficznego.

Haszowanie to jednokierunkowa funkcja matematyczna, która przyjmuje na wejściu ciąg znaków o dowolnej długości (hasło wpisane przez użytkownika), a na wyjściu generuje unikalny ciąg o stałej długości (hasz). Funkcja ta jest jednokierunkowa, co oznacza, że na podstawie wygenerowanego haszu nie da się matematycznie odtworzyć hasła wejściowego.

W projekcie wykorzystano funkcje dostarczane przez moduł bezpieczeństwa `werkzeug.security`:
1.  `generate_password_hash(password)`: Pobiera hasło wpisane przez użytkownika, generuje losową wartość zaburzającą (tzw. sól - salt) i stosuje algorytm PBKDF2 z szyfrowaniem SHA-256. Wynikowy ciąg (zawierający informację o algorytmie, soli oraz samym skrócie) jest zapisywany w bazie danych. Użycie soli gwarantuje, że nawet jeśli dwóch użytkowników użyje takiego samego hasła, ich hasze zapisane w bazie danych będą zupełnie inne.
2.  `check_password_hash(hash, password)`: Pobiera zapisany w bazie danych hasz oraz hasło wpisane przez użytkownika w formularzu logowania. Funkcja wyodrębnia sól z haszu, miesza ją z wpisanym hasłem, przeprowadza proces szyfrowania i porównuje nowo wygenerowany hasz z haszem zapisanym w bazie. Jeśli oba skróty są identyczne, hasło jest poprawne.

#### 5.2.4. Przebieg procesu uwierzytelniania (Login Flow)
Proces logowania użytkownika przebiega według następującego algorytmu:
1.  Użytkownik wysyła żądanie `POST` z formularza logowania, przesyłając login (`username`) oraz hasło (`password`).
2.  Aplikacja otwiera bezpieczne połączenie z bazą danych `users.db` za pomocą funkcji `get_connection()`.
3.  Wykonywane jest zapytanie SQL wyszukujące użytkownika o podanym loginie:
    `SELECT id, username, password_hash FROM users WHERE username = ?`
    Znak zapytania `?` reprezentuje tzw. zapytanie parametryzowane (Prepared Statement), które zabezpiecza aplikację przed atakami typu SQL Injection.
4.  Jeśli użytkownik o podanym loginie istnieje, pobierany jest jego rekord.
5.  Wywoływana jest funkcja `check_password_hash(row["password_hash"], password)`.
6.  W przypadku zgodności haseł następuje wywołanie funkcji `login_user()`, która zapisuje identyfikator użytkownika w sesji przeglądarki (zaszyfrowane ciasteczko sesyjne podpisywane kluczem `SECRET_KEY`). Użytkownik zostaje przekierowany na stronę `/dashboard`.
7.  W przypadku braku użytkownika lub niezgodności haseł generowany jest komunikat błędu (mechanizm `flash` we Flasku), a użytkownik pozostaje na stronie logowania.

---

## 6. Analiza kodu źródłowego pliku app.py (Wyjaśnienie krok po kroku)

Poniżej znajduje się szczegółowe wyjaśnienie działania każdej linii i funkcji w pliku `app.py`.

### 6.1. Sekcja importów (Linie 1–23)
*   `base64`: biblioteka standardowa używana do kodowania danych binarnych (wykresów w formacie PNG) na postać tekstową ASCII, co umożliwia wstrzykiwanie obrazów bezpośrednio do kodu HTML.
*   `os`: interfejs systemu operacyjnego, używany do odczytu zmiennych środowiskowych (np. klucza szyfrującego lub domyślnego hasła administratora).
*   `sqlite3`: wbudowana biblioteka obsługująca bazę danych SQLite.
*   `contextlib.closing`: narzędzie ułatwiające zarządzanie zasobami. Gwarantuje automatyczne zamknięcie połączenia z bazą danych po zakończeniu bloku `with`, nawet w przypadku wystąpienia błędu wykonania.
*   `io.BytesIO`: bufor pamięciowy działający jak plik binarny. Pozwala zapisać wykres wygenerowany przez matplotlib bezpośrednio w pamięci RAM, bez potrzeby tworzenia plików tymczasowych na dysku twardym.
*   `pathlib.Path`: nowoczesna biblioteka do manipulacji ścieżkami w systemie operacyjnym, odporna na różnice w zapisie ścieżek między systemami Windows i Linux.
*   `matplotlib`: główna biblioteka do rysowania wykresów. Linia `matplotlib.use("Agg")` przełącza backend graficzny w tryb bezokienkowy. Jest to krytyczne dla aplikacji webowych, ponieważ zapobiega próbom otwierania przez serwer okien graficznych w systemie operacyjnym, co powodowałoby błędy w środowiskach serwerowych.
*   `pandas`: zaawansowane narzędzie do analizy danych, importowane pod powszechnym aliasem `pd`.
*   `flask`: framework webowy. Importowane komponenty:
    *   `Flask`: klasa bazowa aplikacji,
    *   `flash`: system przesyłania jednorazowych komunikatów między widokami,
    *   `redirect`: funkcja przekierowująca użytkownika pod inny adres URL,
    *   `render_template`: funkcja generująca kod HTML na podstawie szablonu Jinja2,
    *   `request`: obiekt przechowujący dane aktualnego żądania HTTP (np. dane z formularza),
    *   `url_for`: funkcja dynamicznie generująca adresy URL powiązane z funkcjami widoku.
*   `flask_login`: biblioteka zarządzająca sesjami. Importowane komponenty:
    *   `LoginManager`: główna klasa zarządzająca uwierzytelnianiem,
    *   `UserMixin`: klasa bazowa dla modelu użytkownika, dostarczająca standardowe metody wymagane przez Flask-Login (np. `is_authenticated`),
    *   `current_user`: globalny obiekt reprezentujący aktualnie zalogowanego użytkownika,
    *   `login_required`: dekorator zabezpieczający wybrane ścieżki przed dostępem niezalogowanych osób,
    *   `login_user`, `logout_user`: funkcje rejestrujące i wyrejestrowujące sesję użytkownika.
*   `werkzeug.security`: funkcje `generate_password_hash` i `check_password_hash` odpowiedzialne za bezpieczne przetwarzanie haseł przy pomocy algorytmów kryptograficznych.

### 6.2. Definicje zmiennych globalnych (Linie 26–34)
*   `BASE_DIR`: wyznacza ścieżkę do katalogu, w którym znajduje się uruchomiony plik `app.py`. Zapobiega to błędom relatywnych ścieżek dostępu w zależności od tego, z jakiego katalogu uruchomiono proces Pythona.
*   `DATABASE_PATH`: bezwzględna ścieżka do pliku bazy danych SQLite (`users.db`).
*   `DATA_PATH`: bezwzględna ścieżka do pliku źródłowego CSV z danymi GUS.
*   `ANALYSIS_START_YEAR` (2015) i `ANALYSIS_END_YEAR` (2025): stałe definiujące sztywne ramy czasowe analizy statystycznej zgodnie z założeniami projektu.

### 6.3. Konfiguracja aplikacji Flask i LoginManager (Linie 36–45)
Instancja klasy `Flask` jest konfigurowana za pomocą unikalnego klucza `SECRET_KEY`. Klucz ten jest pobierany ze zmiennych środowiskowych systemu operacyjnego, a w przypadku ich braku ustawiana jest bezpieczna wartość domyślna. Klucz ten służy do kryptograficznego podpisywania ciasteczek sesyjnych w celu zapobieżenia ich sfałszowaniu po stronie przeglądarki użytkownika.

Następnie inicjalizowany jest obiekt `LoginManager`, który wiąże się z instancją aplikacji webowej. Ustawiane są parametry przekierowania: w przypadku próby nieautoryzowanego dostępu użytkownik zostanie przekierowany na stronę o nazwie `login` (parametr `login_view`), a na stronie wyświetli się komunikat o określonej kategorii wizualnej.

### 6.4. Klasa użytkownika User (Linie 48–51)
Klasa `User` dziedziczy po `UserMixin`. Reprezentuje ona obiekt zalogowanego użytkownika w pamięci aplikacji. Konstruktor pobiera `user_id` oraz `username`. Rzutowanie `user_id` na ciąg znaków (`str`) jest wymaganiem biblioteki `Flask-Login` w celu zachowania spójności typów przy odczycie z ciasteczek sesyjnych.

### 6.5. Funkcja get_connection (Linie 54–57)
Funkcja ta tworzy i zwraca nowe połączenie z bazą danych SQLite. Linia `connection.row_factory = sqlite3.Row` jest kluczowa: zmienia ona domyślny sposób zwracania rekordów z bazy danych. Zamiast standardowych krotek (gdzie do wartości uzyskuje się dostęp po indeksie numerycznym, np. `row[0]`), wyniki są zwracane jako obiekty przypominające słowniki Pythona. Dzięki temu można odwoływać się do kolumn po ich nazwach (np. `row["username"]`), co znacznie zwiększa czytelność kodu i redukuje ryzyko błędów.

### 6.6. Funkcja inicjalizująca bazę danych init_db (Linie 60–84)
Funkcja ta uruchamia się automatycznie przy starcie aplikacji. Jej zadaniem jest:
1.  Utworzenie tabeli `users` w bazie danych, jeżeli jeszcze nie istnieje.
2.  Sprawdzenie za pomocą zapytania SQL, czy w bazie danych istnieje domyślny użytkownik o loginie `admin`.
3.  Jeśli użytkownik `admin` nie istnieje, funkcja odczytuje domyślne hasło (pobrane ze zmiennej środowiskowej lub ustawia domyślne `admin123`), generuje jego bezpieczny skrót kryptograficzny za pomocą `generate_password_hash` i zapisuje rekord w bazie danych.
4.  Wywołanie `connection.commit()` trwale zapisuje wszystkie zmiany w pliku bazy danych.

### 6.7. Funkcja ładowania użytkownika load_user (Linie 86–95)
Jest to funkcja callback wymagana przez bibliotekę `Flask-Login`. Jest oznaczona dekoratorem `@login_manager.user_loader`. Przeglądarka przy każdym zapytaniu HTTP przesyła ciasteczko sesyjne zawierające zaszyfrowany identyfikator użytkownika. Funkcja ta pobiera ten identyfikator, wykonuje bezpieczne zapytanie do bazy danych SQLite i w przypadku odnalezienia rekordu zwraca obiekt klasy `User`. Dzięki temu w dowolnym miejscu aplikacji można sprawdzić status zalogowania za pomocą obiektu `current_user`.

### 6.8. Funkcja przetwarzania danych load_inflation_data (Linie 98–124)
Funkcja realizuje pełny proces ETL (Extract, Transform, Load) na danych GUS:
*   **Wczytywanie (Extract)**: wywoływana jest funkcja `pd.read_csv`. Parametry `sep=";"` oraz `decimal=","` są kluczowe ze względu na polski standard zapisu danych (średnik jako separator kolumn, przecinek jako separator dziesiętny). Kodowanie `encoding="cp1250"` zapewnia prawidłową interpretację polskich znaków diakrytycznych.
*   **Weryfikacja (Validate)**: program sprawdza zestawem kolumn `required_columns.issubset` czy plik posiada kolumny `Rok` i `Wartość`. Jeśli ich nie ma, generowany jest wyjątek `ValueError`.
*   **Transformacja (Transform)**:
    1.  Filtrowanie lat: metoda `.between` ogranicza wiersze do zakresu 2015–2025.
    2.  Zmiana nazw kolumn na małe litery w celu ujednolicenia kodu.
    3.  Sortowanie chronologiczne i resetowanie indeksów tabeli.
    4.  Weryfikacja kompletności: funkcja sprawdza, czy zbiór zawiera dokładnie po jednym wierszu dla każdego roku z wymaganego zakresu. Zapobiega to błędom w obliczeniach w przypadku uszkodzenia pliku wejściowego.
    5.  Obliczanie inflacji: nowa kolumna `inflacja_proc` powstaje przez odjęcie liczby 100 od wskaźnika GUS (wskaźnik 103.6 staje się wartością 3.6%).
    6.  Obliczanie skumulowanego poziomu cen: wskaźniki cen są dzielone przez 100 w celu uzyskania mnożników (np. 1.036). Metoda `.cumprod()` wykonuje skumulowane mnożenie kolejnych wartości, a wynik jest mnożony przez 100. Pozwala to określić, jak zmienił się poziom cen w odniesieniu do roku bazowego 2014 (rok 2014 = 100%).

### 6.9. Funkcja figure_to_base64 (Linie 127–132)
Funkcja ta realizuje konwersję wykresu wygenerowanego w matplotlib do formatu tekstowego:
1.  Tworzony jest obiekt `BytesIO` służący jako bufor w pamięci RAM.
2.  Metoda `figure.savefig` zapisuje wykres do bufora w formacie graficznym PNG. Parametr `dpi=120` ustawia rozdzielczość, a `bbox_inches="tight"` automatycznie obcina puste marginesy wokół wykresu.
3.  Wykres w matplotlib zostaje zamknięty za pomocą `plt.close(figure)` w celu zwolnienia zasobów pamięci RAM serwera.
4.  Wskaźnik odczytu bufora jest cofany na początek za pomocą `image.seek(0)`.
5.  Dane binarne obrazu są kodowane algorytmem Base64, a następnie dekodowane do standardowego ciągu tekstowego UTF-8, który może być bezpośrednio wklejony do tagu `<img src="data:image/png;base64,...">` w HTML.

### 6.10. Funkcja generowania wykresów create_charts (Linie 135–191)
Funkcja ta konfiguruje parametry estetyczne biblioteki matplotlib (np. czcionki, kolory osi, siatki) i generuje trzy niezależne wykresy:
1.  **Wykres liniowy**: prezentuje przebieg średniorocznej inflacji w badanym okresie. Zawiera linię referencyjną na poziomie 0% (próg między inflacją a deflacją).
2.  **Wykres słupkowy**: przedstawia zmiany cen rok do roku z automatycznym kolorowaniem słupków (kolor czerwony dla inflacji dodatniej, niebieski dla deflacji). Nad każdym słupkiem generowana jest etykieta tekstowa z dokładną wartością liczbową.
3.  **Wykres powierzchniowy (skumulowany)**: prezentuje skumulowaną zmianę poziomu cen w czasie, wykorzystując funkcję `fill_between` w celu wypełnienia obszaru pod wykresem kolorem morskim z przezroczystością.

Funkcja zwraca listę trzech zakodowanych tekstowo obrazów gotowych do wyświetlenia w szablonie.

### 6.11. Funkcja widoku logowania login (Linie 194–215)
Obsługuje adres główny `/` aplikacji dla dwóch metod HTTP:
*   `GET`: jeśli użytkownik jest już zalogowany (`current_user.is_authenticated`), zostaje automatycznie przekierowany na dashboard. W przeciwnym razie renderowany jest szablon formularza logowania (`login.html`).
*   `POST`: wywoływana, gdy użytkownik prześle formularz logowania. Dane są pobierane za pomocą `request.form.get`. Następuje proces walidacji w bazie danych SQLite (zgodnie z algorytmem opisanym w sekcji 5.2.4). W przypadku błędu, funkcja `flash` przekazuje komunikat do szablonu, a strona logowania jest przeładowywana.

### 6.12. Funkcja widoku dashboardu dashboard (Linie 218–234)
Obsługuje adres `/dashboard`. Jest zabezpieczona dekoratorem `@login_required` — próba otwarcia tej strony przez niezalogowaną osobę spowoduje automatyczne przekierowanie do formularza logowania.
Działanie funkcji:
1.  Wczytanie danych z CSV przy użyciu `load_inflation_data()`.
2.  Generowanie wykresów przy użyciu `create_charts()`.
3.  Wyznaczenie rekordu z najwyższą inflacją za pomocą metody `.idxmax()` biblioteki pandas.
4.  Pobranie najnowszego rekordu (ostatni wiersz danych).
5.  Obliczenie skumulowanej zmiany cen (wartość z ostatniego roku pomniejszona o 100%).
6.  Przekazanie wszystkich wyliczonych zmiennych oraz wykresów do szablonu HTML `dashboard.html` za pomocą funkcji `render_template`.

### 6.13. Funkcja wylogowania logout (Linie 237–242)
Obsługuje żądania typu `POST` na adres `/logout`. Dekorator `@login_required` zapobiega wywołaniu tej metody przez osoby trzecie. Funkcja wywołuje `logout_user()`, co usuwa sesję użytkownika z ciasteczek przeglądarki, po czym następuje przekierowanie na stronę logowania. Zastosowanie metody `POST` zamiast prostego linku `GET` chroni przed przypadkowym wylogowaniem użytkownika przez roboty sieciowe lub mechanizmy wstępnego pobierania stron w przeglądarkach.

### 6.14. Sekcja uruchomieniowa (Linie 245–250)
Wywoływana jest funkcja `init_db()` w celu przygotowania bazy danych. Instrukcja warunkowa `if __name__ == "__main__"` sprawdza, czy plik został uruchomiony bezpośrednio (np. poprzez `python app.py`). Jeśli tak, następuje start wbudowanego serwera deweloperskiego Flask. Flaga `debug` jest ustawiana na podstawie zmiennej środowiskowej `FLASK_DEBUG`, co pozwala na elastyczne sterowanie trybem diagnostycznym w środowisku uruchomieniowym.

---

## 7. Wnioski i możliwości dalszego rozwoju

### 7.1. Wnioski z analizy danych
Na podstawie przetworzonych danych GUS z lat 2015–2025 sformułowano następujące wnioski:
*   W latach 2015–2016 w Polsce panowała deflacja (odpowiednio -0.9% oraz -0.6%), co oznacza, że średni poziom cen towarów i usług konsumpcyjnych spadał rok do roku.
*   Od 2017 roku nastąpił powrót do umiarkowanej inflacji, która w roku 2020 (początek pandemii COVID-19) osiągnęła poziom 3.4%.
*   W latach 2022–2023 nastąpił gwałtowny wzrost inflacji, osiągając maksimum w roku 2022 na poziomie 14.4% (najwyższy wskaźnik w badanym okresie), a następnie 11.4% w roku 2023. Było to spowodowane czynnikami makroekonomicznymi i geopolitycznymi.
*   W latach 2024–2025 tempo wzrostu cen uległo wyraźnemu spowolnieniu, stabilizując się na poziomie 3.6% rocznie.
*   Analiza poziomu cen skumulowanych wykazuje, że spadek stopy inflacji (np. z 14.4% do 3.6%) nie oznacza spadku cen w sklepach (deflacji), a jedynie wolniejszy ich wzrost. Wskaźnik skumulowany pokazuje, że koszyk zakupowy w 2025 roku był o ponad 55% droższy w porównaniu do roku 2014.

### 7.2. Możliwości dalszego rozwoju aplikacji
Projekt w obecnej formie w pełni realizuje wszystkie wymagania formalne. W ramach potencjalnego dalszego rozwoju systemu można wdrożyć następujące usprawnienia:
1.  **Rozszerzenie bazy danych**: wdrożenie pełnej rejestracji kont użytkowników z poziomu interfejsu graficznego wraz z weryfikacją siły hasła.
2.  **Dynamiczny wybór zakresu analizy**: dodanie na dashboardzie elementów sterujących (np. suwaków lub pól wyboru), które przekazywałyby parametry żądania do backendu, umożliwiając użytkownikowi dynamiczne definiowanie lat początkowych i końcowych analizy.
3.  **Automatyczna aktualizacja danych (Web Scraping)**: zaimplementowanie modułu pobierającego dane bezpośrednio z API Głównego Urzędu Statystycznego (np. poprzez API Banku Danych Lokalnych) w celu eliminacji konieczności ręcznego aktualizowania pliku CSV w przypadku publikacji nowych odczytów przez GUS.
4.  **Dwuskładnikowe uwierzytelnianie (2FA)**: integracja systemu logowania z protokołem TOTP (np. Google Authenticator) w celu zwiększenia bezpieczeństwa dostępu do danych analitycznych.

---

## 8. Weryfikacja wymagań z pliku projekt.pdf

Poniższa tabela przedstawia mapowanie wymagań określonych przez prowadzącego zajęcia na konkretne elementy zaimplementowane w projekcie.

| Wymaganie z projekt.pdf | Sposób realizacji w projekcie | Status |
|---|---|---|
| 1. Skład zespołu oraz role | Określono w sekcji 1 niniejszej dokumentacji (projekt jednoosobowy, Jakub Liszewski). | Spełniono |
| 2. Opis tematyki projektu | Opisano w sekcji 2 (Analiza inflacji w Polsce w ujęciu rocznym). | Spełniono |
| 3. Cel realizacji projektu | Zdefiniowano w sekcji 3 (Aplikacja analityczno-webowa z bezpiecznym dostępem). | Spełniono |
| 4. Opis realizacji i sposobu osiągnięcia celu | Wyjaśniono szczegółowo w sekcji 4 (Podział na etapy: analityczny, bazodanowy, prezentacyjny). | Spełniono |
| 5. Opis zadań, stosu technologicznego | Wymieniono i opisano w sekcji 5 (Python, Flask, SQLite, pandas, matplotlib). | Spełniono |
| 6. Wnioski i możliwości rozwoju | Zawarto w sekcji 7 (Interpretacja wskaźników inflacji oraz 4 punkty rozwoju aplikacji). | Spełniono |
| 7. Bibliografia i cytowania | Dodano w sekcji 9 w formacie harwardzkim / numerycznym wraz z odnośnikami w tekście. | Spełniono |
| 8. Temat: analiza danych rzeczywistych online | Wykorzystano oficjalny zbiór danych GUS [1], udostępniony na rządowym portalu statystycznym. | Spełniono |
| 9. System logowania oparty o bazę danych | Zaimplementowano bazę SQLite (`users.db`) z tabelą `users` oraz haszowaniem PBKDF2 [4] [5]. | Spełniono |
| 10. Treść analizy po zalogowaniu | Użyto dekoratora `@login_required` w aplikacji Flask. Niezalogowani są przekierowywani na stronę logowania. | Spełniono |
| 11. Indywidualna wizualizacja raportu | Zaprojektowano autorski arkusz stylów CSS, responsywny układ siatek kart oraz 3 spersonalizowane wykresy. | Spełniono |
| 12. Dołączona dokumentacja | Niniejszy plik `DOKUMENTACJA.md` oraz plik instrukcyjny `README.md` są integralną częścią repozytorium. | Spełniono |

---

## 9. Bibliografia

[1] Główny Urząd Statystyczny, *Roczne wskaźniki cen towarów i usług konsumpcyjnych od 1950 roku*. Dostęp online: https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/ [Dostęp: 13.06.2026].

[2] Główny Urząd Statystyczny, *Komunikat w sprawie średniorocznego wskaźnika cen towarów i usług konsumpcyjnych ogółem w 2025 roku*. Dostęp online: https://stat.gov.pl/sygnalne/komunikaty-i-obwieszczenia/lista-komunikatow-i-obwieszczen/komunikat-w-sprawie-sredniorocznego-wskaznika-cen-towarow-i-uslug-konsumpcyjnych-ogolem-w-2025-r-%2C50%2C13.html [Dostęp: 13.06.2026].

[3] Grinberg, M., 2018. *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.

[4] Pallets Projects, *Flask Documentation (v3.0.x)*. Dostęp online: https://flask.palletsprojects.com/ [Dostęp: 13.06.2026].

[5] McKinney, W., 2022. *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter*. O'Reilly Media.

[6] Banasik, A., 2022. *Języki Obiektowe I (Python) - Zajęcia 5*. Materiały dydaktyczne, Wyższa Szkoła Bankowa w Chorzowie.
