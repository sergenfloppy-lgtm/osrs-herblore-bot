@echo off
title OSRS Bot - Simple Click Setup
cls
echo ====================================================================
echo OSRS BOT - SIMPLE CLICK SETUP
echo ====================================================================
echo.
echo NO F8 REQUIRED!
echo.
echo HOW IT WORKS:
echo   1. Bot asks "Click on bank booth"
echo   2. You position your mouse over it
echo   3. Bot captures the position
echo   4. Repeat for all 5 items
echo   5. Bot runs!
echo.
echo MUCH SIMPLER - NO KEYBOARD FOCUS ISSUES!
echo.
echo ====================================================================
echo.
pause

python bot_simple_setup.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
