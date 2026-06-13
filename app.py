import base64
import os
import sqlite3
from contextlib import closing
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "users.db"
DATA_PATH = (
    BASE_DIR
    / "data"
    / "rocznewskaznikicentowarowiuslugkonsumpcyjnychod1950roku_2.csv"
)
ANALYSIS_START_YEAR = 2015
ANALYSIS_END_YEAR = 2025

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "klucz-do-lokalnego-projektu-zaliczeniowego"
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Zaloguj się, aby zobaczyć analizę."
login_manager.login_message_category = "info"


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = str(user_id)
        self.username = username


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    default_password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")

    with closing(get_connection()) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )

        user = connection.execute(
            "SELECT id FROM users WHERE username = ?", ("admin",)
        ).fetchone()

        if user is None:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", generate_password_hash(default_password)),
            )
        connection.commit()


@login_manager.user_loader
def load_user(user_id):
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    if row is None:
        return None
    return User(row["id"], row["username"])


def load_inflation_data():
    source = pd.read_csv(DATA_PATH, sep=";", decimal=",", encoding="cp1250")
    required_columns = {"Rok", "Wartość"}

    if not required_columns.issubset(source.columns):
        raise ValueError("Plik GUS nie zawiera kolumn 'Rok' i 'Wartość'.")

    data = (
        source.loc[
            source["Rok"].between(ANALYSIS_START_YEAR, ANALYSIS_END_YEAR),
            ["Rok", "Wartość"],
        ]
        .rename(columns={"Rok": "rok", "Wartość": "wskaznik_cen"})
        .sort_values("rok")
        .reset_index(drop=True)
    )

    expected_years = list(range(ANALYSIS_START_YEAR, ANALYSIS_END_YEAR + 1))
    if data["rok"].tolist() != expected_years:
        raise ValueError(
            f"Plik GUS musi zawierać po jednym wierszu dla lat "
            f"{ANALYSIS_START_YEAR}-{ANALYSIS_END_YEAR}."
        )

    data["inflacja_proc"] = data["wskaznik_cen"] - 100
    data["poziom_cen"] = (data["wskaznik_cen"] / 100).cumprod() * 100
    return data


def figure_to_base64(figure):
    image = BytesIO()
    figure.savefig(image, format="png", dpi=120, bbox_inches="tight")
    plt.close(figure)
    image.seek(0)
    return base64.b64encode(image.getvalue()).decode("utf-8")


def create_charts(data):
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": "#334155",
            "xtick.color": "#475569",
            "ytick.color": "#475569",
        }
    )

    figure_1, axis_1 = plt.subplots(figsize=(8, 4))
    axis_1.plot(
        data["rok"],
        data["inflacja_proc"],
        color="#1d4ed8",
        marker="o",
        linewidth=2.5,
    )
    axis_1.axhline(0, color="#94a3b8", linewidth=1)
    axis_1.set_title("Średnioroczna inflacja w Polsce")
    axis_1.set_xlabel("Rok")
    axis_1.set_ylabel("Zmiana cen (%)")
    axis_1.grid(axis="y", alpha=0.25)
    axis_1.set_xticks(data["rok"])
    axis_1.tick_params(axis="x", rotation=45)

    colors = ["#dc2626" if value > 0 else "#2563eb" for value in data["inflacja_proc"]]
    figure_2, axis_2 = plt.subplots(figsize=(8, 4))
    bars = axis_2.bar(data["rok"], data["inflacja_proc"], color=colors)
    axis_2.set_title("Porównanie zmian cen rok do roku")
    axis_2.set_xlabel("Rok")
    axis_2.set_ylabel("Zmiana cen (%)")
    axis_2.axhline(0, color="#64748b", linewidth=1)
    axis_2.grid(axis="y", alpha=0.2)
    axis_2.set_xticks(data["rok"])
    axis_2.tick_params(axis="x", rotation=45)
    axis_2.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)

    figure_3, axis_3 = plt.subplots(figsize=(8, 4))
    axis_3.fill_between(
        data["rok"], 100, data["poziom_cen"], color="#0f766e", alpha=0.2
    )
    axis_3.plot(data["rok"], data["poziom_cen"], color="#0f766e", linewidth=2.5)
    axis_3.set_title("Skumulowany poziom cen (2014 = 100)")
    axis_3.set_xlabel("Rok")
    axis_3.set_ylabel("Poziom cen")
    axis_3.grid(axis="y", alpha=0.25)
    axis_3.set_xticks(data["rok"])
    axis_3.tick_params(axis="x", rotation=45)

    return [
        figure_to_base64(figure_1),
        figure_to_base64(figure_2),
        figure_to_base64(figure_3),
    ]


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with closing(get_connection()) as connection:
            row = connection.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            login_user(User(row["id"], row["username"]))
            return redirect(url_for("dashboard"))

        flash("Nieprawidłowy login lub hasło.", "error")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    data = load_inflation_data()
    charts = create_charts(data)
    highest = data.loc[data["inflacja_proc"].idxmax()]
    latest = data.iloc[-1]
    cumulative_change = data.iloc[-1]["poziom_cen"] - 100

    return render_template(
        "dashboard.html",
        charts=charts,
        data=data.to_dict("records"),
        highest=highest,
        latest=latest,
        cumulative_change=cumulative_change,
    )


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Wylogowano poprawnie.", "info")
    return redirect(url_for("login"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
