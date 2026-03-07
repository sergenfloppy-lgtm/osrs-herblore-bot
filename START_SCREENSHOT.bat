@echo off
title OSRS Bot - F8 Screenshot Detection
cls
echo ====================================================================
echo OSRS BOT - F8 SCREENSHOT DETECTION
echo ====================================================================
echo.
echo HOW IT WORKS:
echo   1. Put herbs and vials in inventory
echo   2. Press F8 - bot detects them!
echo   3. Open bank with items visible
echo   4. Press F8 - bot finds them in bank!
echo   5. Close bank and press F8
echo   6. Bot has everything it needs!
echo.
echo FEATURES:
echo   - Uses OpenCV template matching
echo   - Finds items automatically
echo   - Saves templates for reuse
echo   - No manual position entry!
echo.
echo ====================================================================
echo.
pause

python bot_screenshot.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR
    echo ====================================================================
    pause
)
