# Installing Dependencies for OSRS Bot

## The Problem

The bot crashes immediately with:
```
ModuleNotFoundError: No module named 'mss'
```

This means the required Python packages aren't installed.

## Why It Fails

The server doesn't have `pip` (Python package manager) installed.

## Solution Options

### Option 1: Install pip First (Recommended for Production)

```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip

# Then install bot dependencies
cd /root/.openclaw/workspace/osrs-herblore-bot
pip3 install -r requirements.txt
```

### Option 2: Run Bot on Your Local Machine

Since this bot needs to:
- Capture your OSRS game screen
- Control your mouse/keyboard
- See your game window

**It makes more sense to run it locally on the computer where you play OSRS!**

#### Setup on Local Machine:

1. **Copy the bot files** to your gaming computer:
```bash
# Clone from GitHub
git clone https://github.com/sergenfloppy-lgtm/osrs-herblore-bot.git
cd osrs-herblore-bot

# Or download ZIP from GitHub and extract
```

2. **Install Python 3.11+** if not already installed:
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the bot**:
```bash
python main.py
```

### Option 3: Install Packages Manually (Advanced)

If you can't use pip, you'd need to manually download and install each package:
- opencv-python
- numpy  
- pillow
- pyautogui
- mss
- pytesseract
- PyQt6
- scipy

This is not recommended - use pip instead.

## Current Server Limitations

The server hosting the web apps (Resume Builder, Email Dashboard) is **not suitable for running the OSRS bot** because:

1. ❌ **No display** - Server has no GUI/screen to capture
2. ❌ **No OSRS running** - The game isn't installed
3. ❌ **No pip** - Can't install Python packages
4. ❌ **Remote execution** - Can't control your local mouse/keyboard

## Recommendation

**Run the OSRS bot on your Windows/Mac gaming computer:**

1. Clone the repo: `git clone https://github.com/sergenfloppy-lgtm/osrs-herblore-bot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Open OSRS and log in
4. Run the bot: `python main.py`
5. Follow the setup wizard to select your game window

The bot will then:
- Capture your OSRS game screen
- Control your mouse/keyboard
- Train Herblore automatically

---

## Why This Bot Can't Run on a Server

Unlike the web apps (Resume Builder, Email Dashboard) which are web-based and can run anywhere, the OSRS bot is a **desktop automation tool** that needs:

- ✅ A physical display
- ✅ OSRS running on that display
- ✅ Access to mouse/keyboard input
- ✅ Screen capture permissions

These things only exist on your local gaming machine!

---

## Summary

**Web Apps (on server):**
- ✅ Resume Builder - http://178.104.23.189:5174/
- ✅ Email Dashboard - http://178.104.23.189:3000/

**Desktop App (run locally):**
- 🖥️ OSRS Bot - Run on your gaming computer where OSRS is installed

The code is all in GitHub if you want to run it locally!
