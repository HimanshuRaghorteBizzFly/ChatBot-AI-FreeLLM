@echo off
title AI ChatBot & Vision Studio Launcher
echo ========================================================
echo      Launching AI ChatBot & Vision Studio (Streamlit)
echo ========================================================
echo.

IF EXIST .venv\Scripts\python.exe (
    echo Starting Streamlit via .venv Python...
    .venv\Scripts\python.exe -m streamlit run Frontend.py
    goto end
)

where python >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo Starting Streamlit via system Python...
    python -m streamlit run Frontend.py
    goto end
)

echo [ERROR] Python was not found on your system PATH!
echo.
echo To run locally on Windows:
echo 1. Install Python 3.10+ from https://www.python.org/downloads/
echo    (Check the box "Add Python to PATH" during installation)
echo 2. Run: python -m venv .venv
echo 3. Run: .venv\Scripts\pip install -r requirements.txt
echo 4. Double-click run.bat again!
echo.
echo Alternatively, open this project in VS Code using the included Dev Container.
echo.

:end
pause
