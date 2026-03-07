# OSRS Herblore Bot v2

**Misclick Detection | Visual Validation | Single-Click Withdraws**

---

## What's New in v2

### ✅ Misclick Detection
Bot now **verifies every click** by comparing templates:
- Captures what you clicked
- Compares with original setup
- Requires 65% similarity match
- **Retries automatically** if misclick detected

### ✅ Visual Validation Feedback
**You can now SEE what the bot sees!**
- Saves comparison images to `validation_checks/`
- Side-by-side: Current vs Original
- Shows similarity score
- PASS/FAIL status
- Timestamped for debugging

**Example:**
```
validation_checks/herb_153042.png
[Current Screenshot] | [Original Template]
herb | Score: 0.87 | PASS
```

### ✅ Single-Click Withdraws
**Faster banking!**
- **Shift+Click** = Withdraw-All
- No more right-click menus
- 3 clicks → 1 click per item
- More reliable

### ✅ Complete Recipe Reference
New file: **POTION_RECIPES.md**
- 12+ potion recipes from OSRS Wiki
- Herbs, secondaries, XP, levels
- Training paths
- Cost efficiency guide

---

## Features

### Smart Detection
- **Template matching** on every click
- **65% similarity** required to pass
- **Automatic retries** (up to 3 attempts)
- **Visual proof** saved to disk

### Advanced Anti-Cheat
- Bezier curves with easing
- ±10 pixel random offsets
- Variable speed movements
- Random micro-adjustments (35% chance)
- Gaussian delays
- 10% chance of longer break (15-30s)

### XP Tracking
- Real-time potions/XP count
- XP/hour calculation
- Milestones (1k, 5k, 10k, 50k, 100k)
- Runtime tracking
- Final statistics on exit

---

## Quick Start

### 1. Install
```bash
pip install pyautogui mss opencv-python pillow numpy
```

### 2. Run
```bash
python osrs_bot.py
```

Or double-click `START.bat` on Windows.

### 3. Setup (5 clicks)
Bot will ask you to click on:
1. Bank booth
2. Deposit inventory button
3. Herb in bank (e.g., Guam leaf)
4. Secondary in bank (e.g., Eye of newt)
5. First inventory slot

Done! Bot learns everything automatically.

---

## Supported Potions

| Potion | Level | XP | Herb | Secondary |
|--------|-------|-----|------|-----------|
| Attack | 3 | 25 | Guam leaf | Eye of newt |
| Antipoison | 5 | 37.5 | Marrentill | Unicorn horn dust |
| Strength | 12 | 50 | Tarromin | Limpwurt root |
| Restore | 22 | 62.5 | Harralander | Red spiders' eggs |
| Energy | 26 | 67.5 | Harralander | Chocolate dust |
| Prayer | 38 | 87.5 | Ranarr weed | Snape grass |
| Super attack | 45 | 100 | Irit leaf | Eye of newt |
| Super strength | 55 | 125 | Kwuarm | Limpwurt root |
| Super restore | 63 | 142.5 | Snapdragon | Red spiders' eggs |
| Super defence | 66 | 150 | Cadantine | White berries |
| Ranging | 72 | 162.5 | Dwarf weed | Wine of zamorak |
| Saradomin brew | 81 | 180 | Toadflax | Crushed nest |

See **POTION_RECIPES.md** for complete recipe guide!

---

## How It Works

### Banking with Validation
```
[BANKING]
  Opening... (attempt 1)
  [VALIDATE] Checking if bank was clicked...
  📸 Saved: validation_checks/bank_153042.png
  ✅ bank match: 0.82
  
  Depositing...
  
  Withdrawing Guam leaf...
  [VALIDATE] Checking if herb was clicked...
  📸 Saved: validation_checks/herb_153045.png
  ✅ herb match: 0.87
  
  Withdrawing Eye of newt...
  [VALIDATE] Checking if secondary was clicked...
  📸 Saved: validation_checks/secondary_153048.png
  ✅ secondary match: 0.91
  
  ✅ Done
```

### Misclick Detection
If similarity < 65%:
```
  [VALIDATE] Checking if herb was clicked...
  📸 Saved: validation_checks/herb_153045.png
  ❌ herb match: 0.42
  ⚠️  Herb misclick - retrying...
```

Bot automatically retries!

### Making Potions
```
[MAKING]
  Herb... (attempt 1)
  Secondary...
  Space...
  Waiting 17.3s...
  ✅ Done

📊 14 potions | 350 XP | 42,000/hr | 0:00:30
```

---

## Visual Validation

### Where to Find Images
All validation images saved to:
```
validation_checks/
├── bank_153042.png
├── herb_153045.png
├── secondary_153048.png
└── ...
```

### What They Show
Each image contains:
- **Left:** Current screenshot (what bot clicked)
- **Right:** Original template (from setup)
- **Top:** Similarity score + PASS/FAIL

**Example:**
```
[Screenshot of bank]  |  [Original bank template]
bank | Score: 0.82 | PASS
```

### When They're Created
- **Every click** during banking
- **Every validation check**
- **Timestamped** (HHMMSS format)

**You can review these to debug misclicks!**

---

## Single-Click Withdraws

### Old Method (3 clicks)
```
1. Click item (left-click)
2. Click item (right-click for menu)
3. Move down + click "Withdraw-All"
```

### New Method (1 click)
```
1. Shift+Click item
```

**3x faster!** More reliable, fewer errors.

---

## Anti-Cheat Features

### Mouse Movement
- **Cubic Bezier curves** (not straight)
- **Ease-in/ease-out** (human acceleration)
- **Random control points** (±50px variation)
- **Variable speed** (slow start/end, fast middle)
- **Slight overshoot** at destination

### Click Patterns
- **±10 pixel offset** every click
- **35% chance** of micro-adjustment before click
- **Random hold time** (20-80ms)
- **Never same position twice**

### Timing
- **Gaussian delays** (mean ± std deviation)
- **Variable wait times** (16-20s for potions)
- **Random breaks** (5-10s normal, 15-30s occasional)

---

## Stats Tracking

### Real-Time
```
📊 140 potions | 3,500 XP | 42,000/hr | 0:05:00
```

### Milestones
```
🎉 10,000 XP!
```

### Final Stats
```
============================================================
FINAL: 420 potions | 10,500 XP
Runtime: 0:15:23
============================================================
```

---

## Error Recovery

### Automatic Retries
- **3 attempts** per failed action
- **Validates** each click before continuing
- **Retries** if misclick detected

### What Gets Validated
1. **Bank clicked** correctly
2. **Herb clicked** correctly
3. **Secondary clicked** correctly
4. **Items in inventory** after banking

### When It Fails
```
❌ Banking failed
[BOT STOPS]

Check validation_checks/ folder for images!
```

---

## Files

```
osrs-herblore-bot/
├── osrs_bot.py              ← Main bot
├── START.bat                ← Windows launcher
├── README.md                ← This file
├── POTION_RECIPES.md        ← Complete recipe guide
├── bot_config.json          ← Auto-generated (your setup)
├── templates/               ← Auto-generated (validation templates)
│   ├── bank.png
│   ├── herb.png
│   ├── secondary.png
│   └── ...
└── validation_checks/       ← Auto-generated (visual proofs)
    ├── bank_153042.png
    ├── herb_153045.png
    └── ...
```

---

## Troubleshooting

### "Misclick detected"
**Check:** `validation_checks/` for visual proof
- Compare left (clicked) vs right (original)
- Low score = wrong position
- Re-run setup if templates are wrong

### "Validation failing constantly"
**Cause:** Screen changed since setup
**Fix:** Run setup again

### "Bot withdrawing wrong items"
**Cause:** Misclick during banking
**Check:** `validation_checks/` images
**Fix:** Bot automatically retries (up to 3 times)

---

## Safety

### Failsafe
- Move mouse to **top-left corner** to stop
- Or press **Ctrl+C**

### Detection Risk
⚠️ **Use at your own risk**
- Botting violates OSRS ToS
- Can result in ban
- Not 100% undetectable
- Monitor regularly

**Recommendations:**
- Don't run 24/7
- Use alternate accounts
- Take manual breaks
- Review validation images

---

## Performance

**Expected rates** (with anti-cheat + validation):

| Potion | XP/hour | Potions/hour |
|--------|---------|--------------|
| Attack | ~35k | ~1,400 |
| Strength | ~45k | ~900 |
| Prayer | ~75k | ~850 |
| Super attack | ~85k | ~850 |
| Super strength | ~100k | ~800 |
| Ranging | ~135k | ~830 |

*Slightly slower than v1 due to validation checks*

---

## Changelog

### v2.0 (2026-03-07)
- ✅ Misclick detection with template matching
- ✅ Visual validation images saved to disk
- ✅ Single-click withdraws (Shift+Click)
- ✅ Complete recipe reference (POTION_RECIPES.md)
- ✅ Cleaned up repo (deleted 12 old files)
- ✅ Enhanced error messages
- ✅ Better logging

### v1.0 (2026-03-07)
- Initial release
- Basic herblore bot
- Anti-cheat features
- XP tracking

---

## Resources

- **OSRS Wiki:** https://oldschool.runescape.wiki/w/Herblore
- **Recipes:** See POTION_RECIPES.md
- **GitHub:** https://github.com/sergenfloppy-lgtm/osrs-herblore-bot

---

**Educational purposes only. Use at your own risk.**

**Version:** 2.0  
**Last Updated:** 2026-03-07
