# 🪟 Windows Instructions - GUARANTEED TO WORK

## The Problem

When you double-click `bot_simple.py` or run it from PowerShell, **the window closes immediately** so you can't see any error messages.

## ✅ THE SOLUTION (2 Options)

### Option 1: Use the Batch File (EASIEST)

**Just double-click this file:**
```
START_WINDOWS.bat
```

That's it! The window will stay open and show you everything.

---

### Option 2: Run from PowerShell (IF BATCH FILE DOESN'T WORK)

```powershell
# Open PowerShell in the bot folder
# (Right-click folder → "Open in Terminal" or "Open PowerShell here")

# Run this:
python run_windows.py
```

The window will stay open and show:
- ✅ What's installed
- ❌ What's missing
- 📋 How to install missing packages
- 🎮 The bot running

---

## What You'll See

```
======================================================================
OSRS Bot - Windows Launcher
======================================================================

[1/5] Checking files...
✅ Files found

[2/5] Checking Python version...
✅ Python 3.11.9

[3/5] Checking dependencies...
❌ mss             - Screen capture - NOT INSTALLED
❌ pyautogui       - Mouse/keyboard control - NOT INSTALLED
❌ numpy           - Arrays - NOT INSTALLED
❌ PIL             - Image processing - NOT INSTALLED

======================================================================
⚠️  MISSING DEPENDENCIES
======================================================================

To install missing packages, run this command:

    pip install mss pyautogui numpy pillow

Or install everything:
    pip install -r requirements.txt

======================================================================

Continue in DEMO MODE anyway? (y/n):
```

---

## Installing Dependencies

When you see missing packages, run this in PowerShell:

```powershell
pip install mss pyautogui numpy pillow opencv-python scipy
```

Or:

```powershell
pip install -r requirements.txt
```

Then run the bot again!

---

## Troubleshooting

### "pip is not recognized"

Python isn't in your PATH. Fix it:

1. **Find where Python is installed:**
   ```powershell
   where python
   ```
   
2. **Use full path to pip:**
   ```powershell
   C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe -m pip install mss pyautogui numpy pillow
   ```

### "python is not recognized"

Python isn't installed or not in PATH.

**Solution:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **CHECK "Add Python to PATH"** (important!)
4. Install
5. Restart PowerShell

### Bot window still closes immediately

Use the batch file or `run_windows.py` instead:

```powershell
python run_windows.py
```

This keeps the window open no matter what.

---

## Quick Start Summary

1. **Double-click:** `START_WINDOWS.bat`
2. **See what's missing**
3. **Install dependencies:** `pip install mss pyautogui numpy pillow`
4. **Run again:** Double-click `START_WINDOWS.bat`
5. **Done!** ✅

---

## Files Explained

| File | What It Does |
|------|--------------|
| `START_WINDOWS.bat` | Double-click this! Easy launcher |
| `run_windows.py` | Windows-friendly launcher (keeps window open) |
| `bot_simple.py` | The actual bot (but closes window on error) |
| `main.py` | Full version (advanced) |

**Always use `START_WINDOWS.bat` on Windows!**

---

## Still Not Working?

If `START_WINDOWS.bat` doesn't work, open PowerShell and run:

```powershell
python run_windows.py
```

Then copy/paste the FULL output and send it to me. I'll fix it immediately.

---

## Expected Output (When Working)

```
======================================================================
OSRS Bot - Windows Launcher
======================================================================

[1/5] Checking files...
✅ Files found

[2/5] Checking Python version...
✅ Python 3.11.9

[3/5] Checking dependencies...
✅ mss             - Screen capture
✅ pyautogui       - Mouse/keyboard control
✅ numpy           - Arrays
✅ PIL             - Image processing

[4/5] Starting bot...

╔═══════════════════════════════════════╗
║   OSRS Herblore Bot - Simple Mode     ║
║   Educational purposes only           ║
╚═══════════════════════════════════════╝

✅ All dependencies installed!
Running in FULL MODE...

Available Potions:
------------------------------------------------------------
 1. Attack potion        (Lvl  3,  25.0 XP)
 2. Antipoison           (Lvl  5,  37.5 XP)
...

Select potion number (1-11):
```

---

**This WILL work. Just use `START_WINDOWS.bat` or `run_windows.py`!**
