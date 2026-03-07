@echo off
title OSRS Herblore Bot
cls
echo ====================================================================
echo OSRS HERBLORE BOT - PRODUCTION
echo ====================================================================
echo.
echo FEATURES:
echo   - Herb + Secondary directly (no vials)
echo   - Advanced anti-cheat (Bezier curves, variable timing)
echo   - State validation (checks each step)
echo   - Error recovery (retries failed steps)
echo   - XP tracker with milestones
echo   - Smart delays and random breaks
echo.
echo SETUP:
echo   1. Select your potion
echo   2. Click on 5 positions when asked
echo   3. Bot runs automatically!
echo.
echo ====================================================================
echo.
pause

python osrs_bot.py

if errorlevel 1 (
    echo.
    echo ERROR - Check above for details
    pause
)
