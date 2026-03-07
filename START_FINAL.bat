@echo off
title OSRS Bot - FINAL VERSION
cls
echo ====================================================================
echo OSRS BOT - FINAL VERSION
echo ====================================================================
echo.
echo NEW FEATURES:
echo   - Template matching verifies correct items in inventory
echo   - Recognizes items in bank automatically
echo   - PROPER herblore workflow:
echo     1. Make unfinished potions (herb + vial)
echo     2. Add secondary ingredient (eye of newt, etc.)
echo   - SMOOTH Bezier curves with variable speed
echo   - ANTI-CHEAT: Random offsets (+-8px), no exact clicks
echo   - Micro-adjustments before clicks
echo   - Variable delays everywhere
echo.
echo SETUP CAPTURES:
echo   1. Bank booth
echo   2. Deposit button
echo   3. Herb in bank
echo   4. Secondary (eye of newt, etc.)
echo   5. Vials in bank
echo   6. First inventory slot
echo   7. Herb in inventory (for verification)
echo.
echo ====================================================================
echo.
pause

python bot_final.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
