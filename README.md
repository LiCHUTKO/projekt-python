# Analiza inflacji w Polsce

Prosty projekt zaliczeniowy w Pythonie i Flasku. Aplikacja prezentuje analizę
średniorocznej inflacji w Polsce w latach 2015–2025 na podstawie oficjalnych
danych Głównego Urzędu Statystycznego.

## Funkcje

- logowanie użytkownika na podstawie bazy SQLite,
- hasło zapisane w bazie jako bezpieczny hash,
- dashboard dostępny wyłącznie po zalogowaniu,
- trzy wykresy generowane przez `matplotlib`,
- tabela danych wczytana z pliku CSV przez `pandas`,
- automatyczne utworzenie bazy i konta demonstracyjnego.

## Uruchomienie

Wymagany jest Python 3.10 lub nowszy.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Następnie otwórz adres: <http://127.0.0.1:5000>

Dane logowania:

- login: `admin`
- hasło: `admin123`

Przy pierwszym uruchomieniu aplikacja tworzy plik `users.db`. Hasło nie jest
zapisywane jawnie. Można ustawić inne początkowe hasło przed pierwszym
uruchomieniem:

```powershell
$env:DEFAULT_ADMIN_PASSWORD="inne-haslo"
python app.py
```

## Dane

Plik `data/inflacja_gus.csv` zawiera roczne wskaźniki cen towarów i usług
konsumpcyjnych, gdzie rok poprzedni = 100. Kolumna `inflacja_proc` jest różnicą
między wskaźnikiem a wartością 100.

Źródło:

- [GUS – Roczne wskaźniki cen towarów i usług konsumpcyjnych od 1950 r.](https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych)
- [GUS – Sytuacja społeczno-gospodarcza kraju, ceny konsumpcyjne](https://ssgk.stat.gov.pl/01.2025/Ceny_towarow_i_uslug_konsumpcyjnych.html)

Dane pobrano 8 czerwca 2026 r. i zapisano lokalnie, aby projekt działał również
bez połączenia z internetem.

## Struktura

```text
projekt_python/
├── app.py
├── requirements.txt
├── README.md
├── DOKUMENTACJA.md
├── data/
│   └── inflacja_gus.csv
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    └── login.html
```

## Najważniejsze elementy kodu

- `init_db()` tworzy tabelę użytkowników i konto `admin`.
- `login()` sprawdza login i hash hasła.
- `@login_required` chroni stronę `/dashboard`.
- `load_inflation_data()` wczytuje CSV i oblicza skumulowany poziom cen.
- `create_charts()` generuje wykresy jako obrazy PNG wyświetlane w HTML.

Pełne opracowanie projektu znajduje się w pliku `DOKUMENTACJA.md`.
