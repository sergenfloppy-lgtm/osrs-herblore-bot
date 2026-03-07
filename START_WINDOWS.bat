@echo off
title OSRS Herblore Bot
cls
echo ====================================================================
echo OSRS Herblore Bot - Windows Launcher
echo ====================================================================
echo.

python run_windows.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR: Python might not be installed or not in PATH
    echo ====================================================================
    echo.
    echo Try:
    echo 1. Install Python from python.org
    echo 2. Make sure "Add Python to PATH" was checked during install
    echo.
    pause
)
