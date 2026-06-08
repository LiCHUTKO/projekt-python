# Dokumentacja projektu

## Temat projektu

**Analiza danych rzeczywistych statystycznych dostępnych online oraz
przedstawienie wyników w postaci strony internetowej – analiza inflacji
w Polsce w latach 2015–2025.**

## 1. Skład zespołu i role

Poniższe dane należy zastąpić imionami i nazwiskami członków zespołu:

- Osoba 1 – pozyskanie i analiza danych,
- Osoba 2 – backend aplikacji i baza danych,
- Osoba 3 – frontend, wykresy i dokumentacja.

W małym zespole jedna osoba może pełnić wszystkie wymienione role.

## 2. Opis tematyki projektu

Projekt dotyczy zmian średniego poziomu cen towarów i usług konsumpcyjnych
w Polsce. Analizowany wskaźnik CPI jest powszechnie nazywany wskaźnikiem
inflacji. Główny Urząd Statystyczny publikuje jego roczne wartości przy
podstawie „rok poprzedni = 100” [1]. Przykładowo wskaźnik 103,6 oznacza wzrost
średniego poziomu cen o 3,6% w stosunku do poprzedniego roku.

Analiza obejmuje lata 2015–2025. Dane zapisano w lokalnym pliku CSV, dzięki
czemu aplikacja nie wymaga dostępu do internetu podczas prezentacji. Wartości
pochodzą z oficjalnej tabeli GUS [1]. Dodatkowe opracowanie GUS potwierdza
wartości dla lat 2016–2024 i opisuje sposób ich interpretacji [2].

## 3. Cel realizacji projektu

Celem było stworzenie prostej strony internetowej, która łączy analizę
rzeczywistych danych publicznych z podstawowymi elementami aplikacji webowej:
logowaniem, bazą danych, chronionym widokiem oraz wizualizacją wyników.

Cel szczegółowy obejmował:

- przedstawienie zmian inflacji w czytelnej formie,
- pokazanie różnicy między tempem inflacji a skumulowanym poziomem cen,
- zabezpieczenie dashboardu przed dostępem bez logowania,
- przygotowanie projektu łatwego do uruchomienia i zaprezentowania lokalnie.

## 4. Realizacja i osiągnięcie celu

Aplikację wykonano we frameworku Flask. Po uruchomieniu funkcja `init_db()`
tworzy bazę SQLite i domyślnego użytkownika. Hasło jest przekształcane przez
funkcję `generate_password_hash()`, dlatego w bazie nie występuje w postaci
jawnej.

Użytkownik niezalogowany widzi formularz logowania. Po poprawnym sprawdzeniu
loginu i hasła biblioteka Flask-Login zapisuje informację o sesji użytkownika.
Widok dashboardu jest oznaczony dekoratorem `@login_required`, który blokuje
dostęp bez aktywnej sesji.

Biblioteka pandas odczytuje dane z pliku `data/inflacja_gus.csv`. Na ich
podstawie obliczany jest również skumulowany poziom cen, przyjmując 2014 rok
za poziom bazowy równy 100. Matplotlib tworzy trzy wykresy zapisywane w pamięci
jako obrazy PNG i umieszczane bezpośrednio w stronie HTML.

## 5. Zadania, technologie i sposób realizacji

### Pozyskanie danych

Z oficjalnej tabeli GUS wybrano roczne wskaźniki cen dla lat 2015–2025 [1].
Wartości przepisano do prostego pliku CSV. Inflację procentową obliczono jako:

```text
inflacja [%] = wskaźnik cen - 100
```

### Analiza danych

Pandas służy do wczytania tabeli oraz obliczenia skumulowanego poziomu cen.
Dashboard pokazuje wartość najnowszą, maksimum oraz łączną zmianę cen.

### Wizualizacja

Matplotlib generuje:

1. wykres liniowy średniorocznej inflacji,
2. wykres słupkowy porównujący poszczególne lata,
3. wykres skumulowanego poziomu cen przy podstawie 2014 = 100.

### Backend i logowanie

Flask obsługuje adresy URL, formularz i szablony. Flask-Login zarządza sesją.
Wbudowany moduł `sqlite3` przechowuje użytkowników. Werkzeug odpowiada za
tworzenie i sprawdzanie hashy haseł.

### Frontend

Interfejs wykonano w HTML, CSS i Jinja2. Zastosowano neutralne kolory, jeden
główny układ treści i prostą responsywność dla mniejszych ekranów. Projekt nie
korzysta z JavaScriptu ani zewnętrznego frameworka CSS.

### Stos technologiczny

- Python – język projektu,
- Flask – aplikacja internetowa,
- Flask-Login – logowanie i ochrona widoków,
- SQLite – lokalna baza użytkowników,
- pandas – odczyt i przetwarzanie danych,
- matplotlib – tworzenie wykresów,
- HTML, CSS i Jinja2 – warstwa prezentacji.

## 6. Wyniki i wnioski

Najwyższą średnioroczną inflację w badanym okresie odnotowano w 2022 roku:
14,4%. W 2023 roku nadal była wysoka i wyniosła 11,4%. W latach 2024–2025
tempo wzrostu cen spadło do 3,6% rocznie [1].

W latach 2015 i 2016 wskaźnik był niższy niż 100, co oznacza niewielki spadek
średniego poziomu cen. Mimo późniejszego spadku tempa inflacji ceny nie wróciły
do wcześniejszego poziomu. Z obliczeń wykonanych na podstawie danych GUS
wynika, że skumulowany poziom cen wzrósł między końcem 2014 a 2025 rokiem
o około 55,2%.

Projekt spełnia założony cel: prezentuje prawdziwe dane na stronie, wymaga
logowania i działa lokalnie przy niewielkiej liczbie zależności.

## 7. Możliwości dalszego rozwoju

Projekt można rozszerzyć o:

- automatyczne pobieranie najnowszych danych z API lub pliku GUS,
- rejestrację użytkowników i zmianę hasła,
- analizę danych miesięcznych,
- porównanie inflacji z wynagrodzeniami,
- eksport tabeli lub wykresów do pliku PDF.

Rozszerzenia nie są konieczne do działania obecnej wersji.

## 8. Bibliografia

[1] Główny Urząd Statystyczny, „Roczne wskaźniki cen towarów i usług
konsumpcyjnych od 1950 r.”,
<https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych>,
dostęp: 8.06.2026.

[2] Główny Urząd Statystyczny, „Sytuacja społeczno-gospodarcza kraju – Ceny
towarów i usług konsumpcyjnych, dane za 2024 r.”,
<https://ssgk.stat.gov.pl/01.2025/Ceny_towarow_i_uslug_konsumpcyjnych.html>,
dostęp: 8.06.2026.

[3] Pallets Projects, „Flask Documentation”,
<https://flask.palletsprojects.com/>, dostęp: 8.06.2026.

[4] Flask-Login, „Flask-Login Documentation”,
<https://flask-login.readthedocs.io/>, dostęp: 8.06.2026.

[5] pandas, „pandas Documentation”,
<https://pandas.pydata.org/docs/>, dostęp: 8.06.2026.

[6] Matplotlib, „Matplotlib Documentation”,
<https://matplotlib.org/stable/>, dostęp: 8.06.2026.
