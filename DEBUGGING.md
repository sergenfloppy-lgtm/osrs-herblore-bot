# Debugging Guide for OSRS Herblore Bot

## Issue: Bot Stops After Window Selection

The bot is now equipped with comprehensive logging to help debug issues.

## Setup

1. **Install Dependencies** (if not already done):
```bash
cd /root/.openclaw/workspace/osrs-herblore-bot
pip install -r requirements.txt
```

2. **Run the Bot**:
```bash
python main.py
```

## Logging

**All bot activity is logged to files in the `logs/` directory.**

### Log Files
- Location: `logs/bot_YYYYMMDD_HHMMSS.log`
- Each run creates a new log file with timestamp
- Contains DEBUG-level details of every action

### What's Logged
- ✅ Initialization steps
- ✅ Screen capture attempts
- ✅ Inventory detection
- ✅ Banking operations  
- ✅ Potion making steps
- ✅ All errors with stack traces
- ✅ Anti-ban actions

### Reading Logs

**After running the bot:**
```bash
# Find the latest log
ls -lht logs/

# View the log
cat logs/bot_*.log

# Or tail it in real-time (in another terminal)
tail -f logs/bot_*.log
```

## Common Issues

### 1. Bot Stops Immediately After Window Selection

**Check the log file for:**
- `Failed to capture screenshot` - Screen capture not working
- `Inventory empty` - Not detecting items correctly
- `Failed to open bank` - Can't find/click bank

**Most likely cause:** The bot is trying to run but can't detect the game properly because:
- The game window region is incorrect
- OSRS isn't actually running
- The game is minimized or covered

### 2. ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'mss'` (or other modules)

**Solution**:
```bash
pip install -r requirements.txt
```

### 3. Permission Errors

The bot needs permission to:
- Capture your screen
- Control mouse/keyboard
- Read/write files

On some systems, you may need to grant accessibility permissions.

## Test Mode

Test the bot components without running the full bot:

```bash
# Test screen capture (once dependencies are installed)
python test_bot.py
```

## Debug Steps

1. **Check logs immediately after bot stops**:
```bash
tail -20 logs/bot_*.log
```

2. **Look for the last action before stopping**:
```bash
grep -E "ERROR|WARN|Failed" logs/bot_*.log
```

3. **Check if screen capture is working**:
```bash
grep "Screenshot captured" logs/bot_*.log
```

4. **See what the bot thinks inventory status is**:
```bash
grep "Has items in inventory" logs/bot_*.log
```

## Expected Behavior

When working correctly, the log should show:
```
INFO - Initializing bot...
INFO - Bot initialized successfully
INFO - Bot loop starting...
DEBUG - Starting iteration #1
DEBUG - Capturing screen region: (x, y, width, height)
DEBUG - Screenshot captured: (height, width, 3)
DEBUG - Checking if inventory has items...
DEBUG - Has items in inventory: False
INFO - Inventory empty - going to bank
INFO - Banking...
```

## Share Logs for Help

If you need help debugging, share:
1. The full log file from `logs/`
2. What you see on screen when it stops
3. Whether OSRS is actually running

---

## Quick Checklist

Before running the bot:
- [ ] OSRS is running and logged in
- [ ] Standing next to a bank
- [ ] Bank contains herbs and vials
- [ ] Game window is visible (not minimized)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Run bot: `python main.py`
- [ ] Check logs if it stops: `tail logs/bot_*.log`
