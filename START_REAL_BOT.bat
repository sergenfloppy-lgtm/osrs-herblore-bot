@echo off
title OSRS Bot - REAL VERSION (ACTUALLY CLICKS!)
cls
echo ====================================================================
echo OSRS HERBLORE BOT - REAL VERSION
echo ====================================================================
echo.
echo This version ACTUALLY CLICKS - not a simulation!
echo.
echo REQUIREMENTS:
echo   - OSRS open and logged in
echo   - Standing at a bank
echo   - Bank has herbs and vials
echo.
echo SAFETY:
echo   - Move mouse to TOP-LEFT corner to stop (FAILSAFE)
echo   - Or press Ctrl+C
echo.
echo ====================================================================
echo.
pause

python bot_working.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR OCCURRED - Check above for details
    echo ====================================================================
    echo.
    pause
)
