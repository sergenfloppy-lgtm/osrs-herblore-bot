@echo off
title OSRS Bot - Calibrated Version (WORKS!)
cls
echo ====================================================================
echo OSRS BOT - CALIBRATED VERSION
echo ====================================================================
echo.
echo This version LETS YOU define the exact positions!
echo.
echo The bot will:
echo   1. Ask you to move mouse to bank
echo   2. Show you where it will click (you can see it!)
echo   3. Ask you to confirm each position
echo   4. Save your settings for next time
echo.
echo This guarantees it clicks the RIGHT spots!
echo.
echo ====================================================================
echo.
pause

python bot_calibrated.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
