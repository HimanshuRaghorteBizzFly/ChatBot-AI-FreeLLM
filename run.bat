@echo off
title AI ChatBot Launcher
echo ========================================================
echo         Launching AI ChatBot (Streamlit)
echo ========================================================
echo.

IF EXIST .venv\Scripts\python.exe (
    echo Starting Streamlit via .venv Python...
    .venv\Scripts\python.exe -m streamlit run Frontend.py
) ELSE (
    echo .venv not found, trying system python...
    python -m streamlit run Frontend.py
)

pause
