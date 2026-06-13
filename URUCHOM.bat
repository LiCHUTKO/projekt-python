@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   Analiza inflacji w Polsce
echo ========================================
echo.

set "SYSTEM_PYTHON="
where py >nul 2>nul
if not errorlevel 1 set "SYSTEM_PYTHON=py -3"

if not defined SYSTEM_PYTHON (
    where python >nul 2>nul
    if not errorlevel 1 set "SYSTEM_PYTHON=python"
)

if not defined SYSTEM_PYTHON (
    echo BLAD: Python nie jest zainstalowany lub nie znajduje sie w PATH.
    echo Zainstaluj Python ze strony https://www.python.org/downloads/
    echo Podczas instalacji zaznacz opcje "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie lokalnego srodowiska .venv...
    %SYSTEM_PYTHON% -m venv .venv
    if errorlevel 1 (
        echo.
        echo BLAD: Nie udalo sie utworzyc srodowiska .venv.
        pause
        exit /b 1
    )
)

set "VENV_PYTHON=.venv\Scripts\python.exe"

"%VENV_PYTHON%" -c "import flask, flask_login, matplotlib, pandas" >nul 2>nul
if errorlevel 1 (
    echo Instalowanie potrzebnych bibliotek...
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo BLAD: Nie udalo sie zainstalowac bibliotek.
        pause
        exit /b 1
    )
)

echo.
echo Aplikacja: http://127.0.0.1:5000
echo Login: admin
echo Haslo: admin123
echo.
echo Aby zatrzymac aplikacje, nacisnij Ctrl+C.
echo.

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5000'"
"%VENV_PYTHON%" app.py

pause
