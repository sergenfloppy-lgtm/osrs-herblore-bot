@echo off
title OSRS Herblore Bot - PRODUCTION VERSION
cls
echo ====================================================================
echo OSRS HERBLORE BOT - PRODUCTION VERSION
echo ====================================================================
echo.
echo FEATURES:
echo   - Auto-detects RuneLite window
echo   - Auto-finds bank and inventory
echo   - Advanced anti-ban (Bezier curves, breaks, stat checks)
echo   - Retry logic with validation
echo   - Error screenshots
echo   - Zero manual setup
echo.
echo REQUIREMENTS:
echo   - RuneLite client (fixed mode, fully zoomed in)
echo   - Varrock East Bank location
echo   - Logged in with bank access
echo.
echo SAFETY:
echo   - Move mouse to TOP-LEFT corner to stop
echo   - Or press Ctrl+C
echo.
echo ====================================================================
echo.
pause

python bot_production.py

if errorlevel 1 (
    echo.
    echo ====================================================================
    echo ERROR - Check above for details
    echo ====================================================================
    echo.
    pause
)
