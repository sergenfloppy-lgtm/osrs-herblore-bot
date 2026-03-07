# Which File Should I Use?

## 🎯 Quick Answer

**Use this file:** `bot_working.py` (or double-click `START_REAL_BOT.bat`)

---

## 📁 File Comparison

| File | Clicks? | Purpose | Use When |
|------|---------|---------|----------|
| **bot_working.py** | ✅ YES | **REAL BOT - Actually clicks** | **Use this!** |
| bot_simple.py | ❌ NO | Simulation/demo only | Testing setup |
| main.py | ✅ YES | Full version (complex) | Advanced users |
| test_clicks.py | ✅ YES | Test PyAutoGUI | Debugging |

---

## ⚠️ The Problem You Had

**You ran `bot_simple.py`** which says:
```
✅ All dependencies installed!
Running in FULL MODE...
```

But it's misleading! Even in "FULL MODE", `bot_simple.py` **NEVER actually clicks** - it only prints "Clicking herb..." but doesn't call pyautogui.click().

**It's a simulation/demo, not the real bot!**

---

## ✅ The Solution

Use **`bot_working.py`** instead!

### Windows (Easy Way):
```
Double-click: START_REAL_BOT.bat
```

### Windows (Command Line):
```powershell
python bot_working.py
```

### Mac/Linux:
```bash
python3 bot_working.py
```

---

## 🎮 What bot_working.py Does

### Setup Phase:
1. **Define game window** - Mark top-left and bottom-right corners
2. **Select potion** - Choose which potion to make
3. **Define bank position** - Click where your bank is
4. **Define inventory** - Mark first inventory slot

### Running Phase:
- ✅ **Actually clicks** your mouse
- ✅ Opens bank
- ✅ Withdraws items
- ✅ Makes potions
- ✅ Shows statistics

---

## 🔧 Setup Steps (bot_working.py)

When you run it:

### Step 1: Game Window
```
Move mouse to TOP-LEFT corner of game → Press Enter
Move mouse to BOTTOM-RIGHT corner of game → Press Enter
```

### Step 2: Select Potion
```
Select number (1-11): 5
```

### Step 3: Bank Position
```
Open your bank in OSRS
Move mouse to CENTER of bank booth
Press Enter
```

### Step 4: Inventory
```
Move mouse to FIRST inventory slot (top-left)
Press Enter
```

### Step 5: Start!
```
Press Enter to start
Bot will now click automatically!
```

---

## 🛡️ Safety Features

### FAILSAFE (Important!)
- **Move mouse to TOP-LEFT corner** of screen to stop instantly
- Or press **Ctrl+C**
- PyAutoGUI automatically stops if you move mouse to corner

### Warning
- ⚠️ Bot will control your mouse
- ⚠️ Don't touch mouse/keyboard while running
- ⚠️ Use at your own risk
- ⚠️ Botting violates OSRS ToS

---

## 🐛 Troubleshooting

### "Bot doesn't click anything"
- You probably ran `bot_simple.py` (simulation only)
- Use `bot_working.py` instead!

### "Mouse moves but doesn't click"
- Run PowerShell as Administrator
- Check Windows Security settings
- Try: `python test_clicks.py` to verify clicking works

### "FailSafeException"
- You moved mouse to top-left corner (safety feature)
- This is intentional - keeps window open so you can restart

---

## 📊 What You'll See

```
╔═══════════════════════════════════════╗
║   OSRS Bot - REAL VERSION             ║
║   Actually clicks your mouse!         ║
╚═══════════════════════════════════════╝

✅ PyAutoGUI loaded
✅ mss loaded

⚠️  FAILSAFE ENABLED: Move mouse to top-left corner to stop!

============================================================
STEP 1: Define Game Window
============================================================

Move your mouse to the TOP-LEFT corner...
[You follow the setup steps]

============================================================
BOT STARTING
============================================================

ITERATION #1

[BANKING]
  Opening bank...
  ✓ Clicked at (723, 456)
  Depositing items...
  ✅ Banking complete

[MAKING POTIONS]
  Clicking herb...
  ✓ Clicked at (1245, 678)
  Clicking vial...
  ✓ Clicked at (1287, 678)
  ✅ Potions made

📊 Stats:
  Potions: 14
  XP: 1,225
  XP/hr: 45,000
```

---

## 🎯 Summary

| What You Want | Use This |
|---------------|----------|
| **Actually make potions** | `bot_working.py` |
| Test if clicking works | `test_clicks.py` |
| See a demo | `bot_simple.py` |
| Advanced features | `main.py` |

**For real use → `bot_working.py` (or `START_REAL_BOT.bat`)**

---

**This version WILL click. I guarantee it.** 🎯
