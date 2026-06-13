# Specyfikacja techniczna źródła danych statystycznych

## 1. Identyfikacja pliku źródłowego

Dane wejściowe wykorzystywane przez moduł analityczny aplikacji są przechowywane w następującej lokalizacji w strukturze repozytorium:

```
data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv
```

Plik ten stanowi oficjalny rejestr statystyczny publikowany przez Główny Urząd Statystyczny (GUS) w ramach monitoringu cen towarów i usług konsumpcyjnych w Polsce.

---

## 2. Metadane i charakterystyka techniczna zbioru danych

Poniższa tabela przedstawia parametry techniczne pliku CSV:

| Parametr techniczny | Wartość parametru | Opis i znaczenie techniczne |
|---|---|---|
| Podmiot odpowiedzialny | Główny Urząd Statystyczny (GUS) | Centralny organ administracji rządowej odpowiedzialny za zbieranie i udostępnianie informacji statystycznych. |
| Format pliku | CSV (Comma-Separated Values) | Tekstowy format zapisu danych tabelarycznych, w którym każdy wiersz pliku odpowiada jednemu rekordowi tabeli. |
| Kodowanie znaków | Windows-1250 (CP1250) | Jednobajtowe kodowanie przeznaczone do zapisu tekstów w językach środkowoeuropejskich używających alfabetu łacińskiego (w tym polskich znaków diakrytycznych). |
| Separator kolumn | Średnik (`;`) | Znak używany do rozdzielania poszczególnych pól w obrębie jednego wiersza (standard europejski dla formatów CSV). |
| Separator dziesiętny | Przecinek (`,`) | Znak rozdzielający część całkowitą liczby od jej części ułamkowej (standard zapisu liczb w Polsce). |
| Całkowity zakres czasowy | 1950–2025 | Pełna seria czasowa dostarczana w oryginalnym pliku GUS (76 wierszy). |
| Zakres czasowy analizy | 2015–2025 | Zakres odfiltrowywany i przetwarzany przez aplikację (11 wierszy). |

---

## 3. Czym jest format CSV i jak działa w ujęciu technicznym

Format CSV (Comma-Separated Values) jest tekstowym formatem reprezentacji danych tabelarycznych. Każdy wiersz pliku reprezentuje jeden wiersz tabeli, a poszczególne kolumny wewnątrz tego wiersza są oddzielone znakiem rozdzielającym (separatorem). 

W krajach anglosaskich standardowym separatorem kolumn jest przecinek (`,`), a separatorem dziesiętnym w liczbach zmiennoprzecinkowych jest kropka (`.`). W krajach europejskich (w tym w Polsce), ze względu na powszechne stosowanie przecinka jako separatora dziesiętnego (np. w zapisie 103,6), zastosowanie przecinka jako separatora kolumn powodowałoby niejednoznaczność interpretacji struktury tabeli. Z tego powodu jako separator kolumn stosuje się średnik (`;`), co pozwala zachować przecinki wewnątrz wartości liczbowych.

---

## 4. Kodowanie znaków Windows-1250 (CP1250)

Plik źródłowy GUS został zakodowany w standardzie Windows-1250. Jest to standard kodowania znaków opracowany przez firmę Microsoft dla systemów z rodziny Windows, mający na celu obsługę języków środkowoeuropejskich. 

W przeciwieństwie do nowoczesnego kodowania Unicode (np. UTF-8), w którym znaki mogą być zapisywane na różnej liczbie bajtów (od 1 do 4), w kodowaniu Windows-1250 każdy znak zajmuje dokładnie 1 bajt (8 bitów). Pozwala to na zakodowanie maksymalnie 256 unikalnych znaków. Wartości od 0 do 127 są zgodne ze standardem ASCII (podstawowe litery alfabetu łacińskiego bez znaków narodowych), natomiast wartości od 128 do 255 zawierają znaki specyficzne dla danego regionu, takie jak polskie litery diakrytyczne: ą, ć, ę, ł, ń, ó, ś, ź, ż (zarówno małe, jak i wielkie).

Próba wczytania pliku o kodowaniu Windows-1250 za pomocą domyślnego dla wielu systemów kodowania UTF-8 skutkuje błędami interpretacji znaków diakrytycznych (tzw. "krzakami" lub błędami dekodowania, np. znak "ł" czy "ó" staje się nieczytelny). W programie Python wczytywanie pliku jest jawnie sparametryzowane parametrem `encoding="cp1250"`, co zapobiega tym błędom.

---

## 5. Struktura kolumn pliku wejściowego

Plik CSV zawiera następujące kolumny:

1.  **Nazwa zmiennej**: przechowuje stałą wartość tekstową opisującą rodzaj badanego wskaźnika. W tym przypadku jest to "Wskaźnik cen towarów i usług konsumpcyjnych".
2.  **Jednostka terytorialna**: wskazuje obszar geograficzny, którego dotyczy badanie. Wartość dla wszystkich rekordów to "Polska".
3.  **Sposób prezentacji**: definiuje bazę odniesienia dla podawanego wskaźnika. Wartość "Rok poprzedni = 100" wskazuje, że odczyt dla każdego roku jest relacją do cen z roku bezpośrednio go poprzedzającego.
4.  **Rok**: rok kalendarzowy, dla którego wyznaczono wskaźnik (liczba całkowita).
5.  **Wartość**: wartość wskaźnika cen (liczba zmiennoprzecinkowa).
6.  **Flaga**: kolumna zawierająca ewentualne oznaczenia dodatkowe stosowane przez GUS (w analizowanym zbiorze pozostaje pusta).

---

## 6. Interpretacja matematyczna wskaźnika GUS

Wskaźnik cen podawany w relacji "Rok poprzedni = 100" interpretuje się następująco:
*   Wartość wskaźnika wynosząca **dokładnie 100.0** oznacza brak średniej zmiany poziomu cen w stosunku do roku ubiegłego (cena koszyka zakupowego nie zmieniła się).
*   Wartość wskaźnika **powyżej 100.0** oznacza wzrost cen (inflację). Wartość procentową inflacji oblicza się odejmując 100 od wskaźnika.
*   Wartość wskaźnika **poniżej 100.0** oznacza spadek cen (deflację). Wartość procentową deflacji (jako spadek ujemny) również wyznacza się poprzez odjęcie 100 od wskaźnika.

### 6.1. Przykłady obliczeniowe:

*   **Rok 2015**: Wartość wskaźnika wynosi `99.1`.
    $$\text{Inflacja} = 99.1 - 100.0 = -0.9\%$$
    Wystąpił spadek cen o 0.9% (deflacja).
*   **Rok 2022**: Wartość wskaźnika wynosi `114.4`.
    $$\text{Inflacja} = 114.4 - 100.0 = 14.4\%$$
    Wystąpił wzrost cen o 14.4% (inflacja).
*   **Rok 2025**: Wartość wskaźnika wynosi `103.6`.
    $$\text{Inflacja} = 103.6 - 100.0 = 3.6\%$$
    Wystąpił wzrost cen o 3.6% (inflacja).

---

## 7. Wczytywanie danych w bibliotece pandas

W kodzie aplikacji (plik `app.py`, funkcja `load_inflation_data`) wczytanie pliku realizowane jest za pomocą instrukcji:

```python
source = pd.read_csv(DATA_PATH, sep=";", decimal=",", encoding="cp1250")
```

Argumenty funkcji `read_csv`:
*   `DATA_PATH`: obiekt ścieżki (z klasy `Path`) wskazujący lokalizację pliku.
*   `sep=";"`: informuje parser biblioteki pandas, że kolumny w pliku są rozdzielane średnikami.
*   `decimal=","`: informuje parser, że w wartościach liczbowych przecinek pełni rolę separatora dziesiętnego, co pozwala na automatyczną konwersję tekstowych reprezentacji liczb (np. "103,6") na zmiennoprzecinkowy typ numeryczny w Pythonie (`float64`).
*   `encoding="cp1250"`: określa zestaw kodowania znaków niezbędny do prawidłowego odczytu polskich liter.

---

## 8. Zasada pojedynczego źródła prawdy (Single Source of Truth)

Architektura projektu opiera się na zasadzie jednego źródła prawdy. Oznacza to, że aplikacja pobiera dane bezpośrednio z jednego, pełnego pliku CSV dostarczonego przez GUS. W repozytorium nie ma żadnych innych plików zawierających kopie lub fragmenty tych samych danych statystycznych. Wszystkie operacje filtrowania (wybór lat 2015–2025) oraz obliczeń matematycznych (inflacja procentowa, skumulowany poziom cen) są wykonywane programowo przy każdym uruchomieniu aplikacji. Zapobiega to powstawaniu rozbieżności danych w przypadku ewentualnej aktualizacji pliku źródłowego.
