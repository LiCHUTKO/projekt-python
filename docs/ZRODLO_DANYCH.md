# Źródło danych

## Plik źródłowy

```
data/rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv
```

## Pochodzenie

Plik pochodzi z oficjalnej publikacji Głównego Urzędu Statystycznego:

**Roczne wskaźniki cen towarów i usług konsumpcyjnych od 1950 roku**

🔗 https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/

## Metadane pliku

| Właściwość | Wartość |
|---|---|
| Źródło | Główny Urząd Statystyczny (GUS) |
| Format | CSV |
| Separator kolumn | `;` (średnik) |
| Separator dziesiętny | `,` (przecinek) |
| Kodowanie | Windows-1250 (cp1250) |
| Zakres lat | 1950–2025 |
| Liczba wierszy danych | 76 |
| Analizowany zakres | 2015–2025 (11 wierszy) |

## Kolumny

| Kolumna | Opis |
|---|---|
| `Nazwa zmiennej` | Nazwa wskaźnika statystycznego |
| `Jednostka terytorialna` | Kraj (Polska) |
| `Sposób prezentacji` | Podstawa wskaźnika (rok poprzedni = 100) |
| `Rok` | Rok, którego dotyczy wskaźnik |
| `Wartość` | Wskaźnik cen (100 = brak zmiany, >100 = wzrost, <100 = spadek) |
| `Flaga` | Ewentualne oznaczenia GUS (puste w tym pliku) |

## Jak rozumieć wskaźnik

GUS podaje wartości przy podstawie **rok poprzedni = 100**:

- `103,6` → ceny wzrosły średnio o **3,6%**
- `99,1` → ceny spadły średnio o **0,9%**
- `100,0` → brak zmiany

Aplikacja oblicza inflację procentową:

```
inflacja [%] = Wartość − 100
```

## Data pobrania

Plik został pobrany ze strony GUS w czerwcu 2026 roku.
Dane za 2025 rok są zgodne z komunikatem GUS o średniorocznym wskaźniku
cen towarów i usług konsumpcyjnych w 2025 r. (103,6).

## Uwaga o integralności

Projekt celowo korzysta z **jednego** pliku źródłowego GUS. Nie istnieje
drugi, ręcznie skrócony plik z wybranymi latami. Dzięki temu w repozytorium
istnieje jedno źródło prawdy — eliminuje to ryzyko rozbieżności danych.
