@echo off
title OSRS Bot - F-Key Setup (Simple!)
cls
echo ====================================================================
echo OSRS BOT - F-KEY SETUP
echo ====================================================================
echo.
echo HOW IT WORKS:
echo   1. Bot tells you what to do
echo   2. You move your mouse to the position
echo   3. Press F to save it
echo   4. Repeat for all positions
echo   5. Bot runs!
echo.
echo POSITIONS TO SET UP:
echo   - Bank booth
echo   - Deposit inventory button
echo   - Herb in bank
echo   - Vials in bank
echo   - First inventory slot
echo.
echo SAVES YOUR SETUP: You only do this once!
echo.
echo ====================================================================
echo.
pause

python bot_fkey.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
