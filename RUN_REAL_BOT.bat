@echo off
title OSRS Herblore Bot - REAL VERSION
cls
echo ====================================================================
echo OSRS HERBLORE BOT - REAL VERSION (ACTUALLY CLICKS!)
echo ====================================================================
echo.
echo WARNING: This will control your mouse and keyboard!
echo.
echo Make sure:
echo   1. OSRS is open and logged in
echo   2. Standing at a bank
echo   3. Bank has herbs and vials
echo.
echo Press Ctrl+C at any time to stop
echo.
pause
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR OCCURRED
    echo ====================================================================
    echo.
    pause
)
