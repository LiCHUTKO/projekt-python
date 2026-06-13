# Analiza inflacji w Polsce 📊

Aplikacja webowa we **Flasku** analizująca oficjalne dane GUS dotyczące
średniorocznych wskaźników cen towarów i usług konsumpcyjnych w Polsce
w latach 2015–2025.

## ✨ Funkcje

- 🔐 logowanie z hasłem hashowanym w SQLite,
- 📈 trzy interaktywne wykresy (Matplotlib),
- 📋 tabela z pełnymi danymi,
- 📊 karty z najważniejszymi statystykami,
- 🎨 responsywny, nowoczesny interfejs CSS,
- 🖥️ skrypt `URUCHOM.bat` do startu jednym kliknięciem.

## 🚀 Szybki start (Windows)

1. Zainstaluj **Python 3.10+** z [python.org](https://www.python.org/downloads/).
2. Kliknij dwa razy `URUCHOM.bat`.
3. Przeglądarka otworzy http://127.0.0.1:5000.
4. Zaloguj się:

```
login: admin
hasło: admin123
```

## 🛠️ Uruchomienie ręczne

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## 📁 Struktura projektu

```
projekt_python/
├── app.py                  # Backend Flask — serwer, logowanie, analiza, wykresy
├── requirements.txt        # Zależności Python
├── URUCHOM.bat             # Skrypt startowy Windows (one-click)
├── .gitignore              # Pliki ignorowane przez Git
│
├── data/                   # Dane źródłowe
│   └── *.csv               # Oficjalny plik GUS z wskaźnikami cen od 1950 r.
│
├── docs/                   # Dokumentacja projektu
│   ├── README.md           # Szczegółowa instrukcja i opis
│   ├── DOKUMENTACJA.md     # Pełna dokumentacja (wymagania, analiza, wnioski)
│   ├── ZRODLO_DANYCH.md    # Opis źródła danych i metadane pliku CSV
│   ├── projekt.pdf         # Oryginalne wymagania prowadzącego
│   └── screenshots/        # Zrzuty ekranu aplikacji
│
├── static/                 # Pliki statyczne
│   └── style.css           # Stylowanie i responsywność
│
└── templates/              # Szablony HTML (Jinja2)
    ├── base.html           # Szablon bazowy (nagłówek, stopka)
    ├── login.html          # Strona logowania
    └── dashboard.html      # Dashboard z analizą
```

## 📚 Dokumentacja

| Dokument | Opis |
|---|---|
| [docs/README.md](docs/README.md) | Szczegółowa instrukcja uruchomienia i opis funkcji |
| [docs/DOKUMENTACJA.md](docs/DOKUMENTACJA.md) | Pełna dokumentacja projektu (cel, analiza, wnioski, bibliografia) |
| [docs/ZRODLO_DANYCH.md](docs/ZRODLO_DANYCH.md) | Informacja o źródle danych GUS |
| [docs/projekt.pdf](docs/projekt.pdf) | Wymagania prowadzącego |

## 🔧 Technologie

| Technologia | Zastosowanie |
|---|---|
| Python 3.10+ | Główny język programowania |
| Flask | Serwer WWW, routing, szablony Jinja2 |
| Flask-Login | Sesje, logowanie, ochrona widoków |
| SQLite | Lokalna baza użytkowników |
| pandas | Odczyt i analiza danych CSV |
| Matplotlib | Generowanie wykresów |
| Werkzeug | Hashowanie haseł |

## 📄 Źródło danych

Oficjalne dane Głównego Urzędu Statystycznego:
[Roczne wskaźniki cen towarów i usług konsumpcyjnych](https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/)

## 👤 Autor

**Jakub Liszewski** — projekt zaliczeniowy z przedmiotu Języki Obiektowe I (Python).
