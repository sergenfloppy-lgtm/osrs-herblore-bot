# OSRS Herblore Bot - Production Release

**Simple. Validated. Anti-Cheat.**

---

## Features

### ✅ Direct Herb + Secondary Workflow
- No vials of water needed
- Herb + Secondary = Finished potion
- Simplified process

### ✅ Advanced Anti-Cheat
- **Bezier curves** with ease-in/ease-out
- **Random offsets**: ±10 pixels every click
- **Variable speed**: Slow at start/end, fast in middle
- **Micro-adjustments**: 35% chance before clicks
- **Random control points**: ±50px variation
- **Gaussian delays**: Natural timing variation
- **Random breaks**: 10% chance of 15-30s break

### ✅ State Validation
- **Bank verification**: Checks bank actually opened
- **Make-X validation**: Confirms interface appeared
- **Inventory checks**: Verifies items withdrawn
- **Template matching**: >60% similarity required

### ✅ Error Recovery
- **3 retries** per failed step
- **Automatic rollback** on validation failures
- **Smart retry logic**: Waits and tries again

### ✅ XP Tracker
- **Total XP** and **XP/hour**
- **Potions made** and **potions/hour**
- **Runtime tracking**
- **Milestones**: 1k, 5k, 10k, 50k, 100k XP
- **Final stats** on exit

---

## Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install pyautogui mss opencv-python pillow numpy
```

### 2. Run Bot
```bash
python osrs_bot.py
```

Or double-click `START.bat` on Windows.

### 3. Follow Setup
Bot will ask you to click on 5 positions:
1. Bank booth
2. Deposit inventory button
3. Herb in bank (e.g., Guam leaf)
4. Secondary in bank (e.g., Eye of newt)
5. First inventory slot

Bot calculates everything else automatically!

---

## Supported Potions

| Potion | Herb | Secondary | Level | XP |
|--------|------|-----------|-------|-----|
| Attack potion | Guam leaf | Eye of newt | 3 | 25 |
| Strength potion | Tarromin | Limpwurt root | 12 | 50 |
| Restore potion | Harralander | Red spiders' eggs | 22 | 62.5 |
| Prayer potion | Ranarr weed | Snape grass | 38 | 87.5 |
| Super attack | Irit leaf | Eye of newt | 45 | 100 |
| Super strength | Kwuarm | Limpwurt root | 55 | 125 |
| Super restore | Snapdragon | Red spiders' eggs | 63 | 142.5 |
| Super defence | Cadantine | White berries | 66 | 150 |
| Ranging potion | Dwarf weed | Wine of zamorak | 72 | 162.5 |

---

## How It Works

### Banking
1. Opens bank
2. **Validates**: Bank interface appeared
3. Deposits inventory
4. Withdraws 14 herbs
5. Withdraws 14 secondaries
6. **Validates**: Inventory has items
7. If validation fails: **Retry** (up to 3 times)

### Making Potions
1. Clicks herb in inventory
2. Clicks secondary in inventory
3. **Validates**: Make-X interface appeared
4. Presses space to start
5. Waits for completion
6. If validation fails: **Retry**

### Stats
```
📊 STATS:
   Potions: 140
   Total XP: 3,500
   XP/hour: 42,000
   Potions/hour: 168.0
   Runtime: 0:05:00
```

---

## Anti-Cheat Details

### Mouse Movement
- **Cubic Bezier curves** (not straight lines)
- **Ease-in/ease-out** (human acceleration)
- **Random control points** every movement
- **Variable speed** along path
- **Slight overshoot** at end (10% of movement)

### Click Patterns
- **±10 pixel offset** on EVERY click
- **Micro-adjustments** before 35% of clicks
- **Random hold time**: 20-80ms
- **Never clicks exact same spot twice**

### Timing
- **Gaussian delays**: Mean ± variation
- **Variable wait times**: 16-20s for potions
- **Random breaks**: 5-10s normally, 15-30s occasionally
- **No predictable patterns**

---

## Safety

### Failsafe
- Move mouse to **top-left corner** to stop instantly
- Or press **Ctrl+C**

### Detection Risk
While this bot includes anti-cheat features:
- ⚠️ **Use at your own risk**
- ⚠️ **Botting violates OSRS ToS**
- ⚠️ **Can result in ban**
- ⚠️ **Not 100% undetectable**

**Recommendations:**
- Don't run 24/7
- Use on alternate accounts
- Monitor regularly
- Take manual breaks

---

## Files

```
osrs-herblore-bot/
├── osrs_bot.py          ← Main bot
├── START.bat            ← Windows launcher
├── bot_config.json      ← Your setup (auto-generated)
├── templates/           ← Validation templates (auto-generated)
│   ├── bank_interface.png
│   ├── makex_interface.png
│   └── [other positions].png
└── README.md            ← This file
```

---

## Troubleshooting

### "Missing dependency"
```bash
pip install pyautogui mss opencv-python pillow numpy
```

### "Bank didn't open"
- Make sure you clicked the right spot during setup
- Try re-running setup
- Stand closer to bank

### "Make-X didn't appear"
- Check inventory has both items
- Herb must be in slot 1
- Secondary must be in slot 15

### "Inventory empty"
- Check bank has items
- Make sure you clicked correct positions
- Try withdrawing manually first to test

---

## Performance

**Expected rates** (with all anti-cheat features enabled):

| Potion | XP/hour | Potions/hour |
|--------|---------|--------------|
| Attack | ~35k | ~1,400 |
| Strength | ~45k | ~900 |
| Prayer | ~75k | ~850 |
| Super attack | ~85k | ~850 |
| Super strength | ~100k | ~800 |

*Actual rates vary based on delays and breaks*

---

## License

Educational purposes only.

Botting violates Old School RuneScape Terms of Service.

Use at your own risk.

---

**GitHub**: https://github.com/sergenfloppy-lgtm/osrs-herblore-bot

**Version**: 1.0 Production

**Last Updated**: 2026-03-07
