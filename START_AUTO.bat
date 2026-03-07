@echo off
title OSRS Bot - AUTO VERSION (Research-Based)
cls
echo ====================================================================
echo OSRS BOT - AUTO-DETECTION VERSION
echo ====================================================================
echo.
echo Based on research of working OSRS bots:
echo   - Uses FIXED coordinates for RuneLite fixed mode
echo   - Inventory slots calculated automatically
echo   - Bank detection using color matching
echo   - Bezier curve movements
echo.
echo REQUIREMENTS:
echo   - RuneLite in FIXED mode
echo   - Fully zoomed in
echo   - At Varrock East Bank
echo.
echo ====================================================================
echo.
pause

python bot_auto.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
