# OSRS Herblore Bot v4

**Dialogue Validation | Visual Overlay | One-Click Recording | Smart Learning**

---

## 🆕 What's New in v4

### ✅ Dialogue Box Validation (Failsafe!)
**Bot now checks if Make-X dialogue appeared after clicking ingredients!**

**The Problem (v3):**
```
1. Click herb ✓
2. Click secondary (misclick!) ✗
3. Press Space → Nothing happens!
4. Wait 20 seconds... (wasted)
```

**The Solution (v4):**
```
1. Click herb ✓
2. Click secondary... 
3. CHECK: Did Make-X dialogue appear?
   ❌ No dialogue detected!
   ⚠️  Retrying... (auto-recovery)
4. Click secondary (correct this time) ✓
5. CHECK: Dialogue appeared! ✅
6. Press Space → Success!
```

**How it works:**
```python
def check_dialogue_appeared():
    # Capture center of screen (400×300 px)
    screenshot = capture_center()
    
    # Check for dialogue characteristics:
    1. Dark background? (avg brightness < 80)
    2. Text present? (edge density > 0.05)
    3. OSRS UI colors? (brown HSV range)
    
    return (dark AND text) OR ui_present
```

**Benefits:**
- ✅ Catches failed secondary clicks
- ✅ Auto-retries (up to 3 times)
- ✅ Prevents wasted inventory
- ✅ Saves failed checks to `validation_checks/dialogue_*.png`

---

### ✅ Visual Overlay
**See exactly where the bot will click!**

**Before starting the bot, you get a visual preview:**

```
overlay_preview.png shows:
┌─────────────────────────────────┐
│                                 │
│  🏦 [Yellow Square] ← Bank      │
│      Red + at center            │
│      ±15px click zone           │
│                                 │
│  🌿 [Yellow Square] ← Herb      │
│      Shows variance area        │
│                                 │
│  🧪 [Yellow Square] ← Secondary │
│                                 │
└─────────────────────────────────┘
```

**Features:**
- Yellow squares = ±15px click variance
- Red crosshairs = exact center position
- Labels for each click zone
- Semi-transparent overlay
- Shows before bot runs

**Why this matters:**
- See if click zones overlap
- Verify positions are correct
- Understand variance visually
- Debug setup issues

---

### ✅ One-Click Recording Mode
**Easiest setup ever! No more Enter spam.**

**Old Setup (v3):**
```
Press Enter → Wait 3s → Move mouse → Click → Confirm
Press Enter → Wait 3s → Move mouse → Click → Confirm
Press Enter → Wait 3s → Move mouse → Click → Confirm
(5 times...)
```

**New Setup (v4):**
```
Press Enter once → Just click everything!

1. Click bank booth     [auto-captured] ✓
2. Click deposit button [auto-captured] ✓
3. Click herb           [auto-captured] ✓
4. Click secondary      [auto-captured] ✓
5. Click inv slot       [auto-captured] ✓

Done!
```

**How it works:**
- Uses `pynput` library for event listening
- Mouse listener captures every click
- Keyboard listener records key presses
- Automatically advances to next step
- No manual confirmation needed

**Benefits:**
- **3x faster** setup
- More natural workflow
- No waiting between steps
- Real-time feedback
- Just click as you normally would

---

### ✅ Enhanced Validation Learning
**Validation adapts to your click variance!**

**The Problem:**
```
High variance (±15px) = clicks further from center
→ Template similarity lower
→ Validation fails even when correct
```

**The Solution:**
```python
# Adjust threshold based on variance
variance = 15  # pixels
threshold = 0.65 - (variance / 150)
# = 0.65 - 0.10 = 0.55 (more lenient)

# More variance = lower threshold (easier to pass)
# Less variance = higher threshold (stricter)
```

**Example:**
```
Variance  | Threshold | Meaning
----------|-----------|----------------------------------
±10 px    | 0.58      | Stricter (clicks near center)
±15 px    | 0.55      | Lenient (clicks spread out)
±20 px    | 0.52      | Very lenient (wide spread)
```

**Benefits:**
- Validation learns from variance
- Fewer false negatives
- More reliable detection
- Adapts to your setup

---

### ✅ Updated Potion-Making Instructions
**Clear 5-step process with validation!**

```
⚗️  [MAKING POTIONS]
   📝 Step 1: Click herb in inventory
   📝 Step 2: Click secondary in inventory
   📝 Step 3: Wait for Make-X dialogue ← NEW!
   📝 Step 4: Press Space to confirm
   📝 Step 5: Wait for potions to finish

Step 1: Clicking herb... (attempt 1/3)
Step 2: Clicking Eye of newt...
Step 3: Checking for Make-X dialogue...
  [VALIDATE] Checking for makex dialogue...
  ✅ Dialogue check: dark=True, text=True, ui=True
Step 4: Pressing Space to confirm...
Step 5: ⏳ Crafting potions (18.3s)...
✅ Potions complete
```

**What you see during runtime:**
- Current step number
- What's happening
- Validation results
- Progress indicators
- Success/failure status

---

## Features

### All v3 Features Plus:
- ✅ Position variance (never same click)
- ✅ Smooth Bezier movement
- ✅ Misclick detection
- ✅ Visual validation images
- ✅ Single-click withdraws
- ✅ XP tracking
- ✅ Anti-ban behaviors

### New v4 Features:
- ✅ Dialogue box validation
- ✅ Visual overlay preview
- ✅ One-click recording setup
- ✅ Adaptive validation threshold
- ✅ Enhanced potion-making flow
- ✅ Better error messages
- ✅ pynput event listeners

---

## Quick Start

### 1. Install
```bash
pip install pyautogui mss opencv-python pillow numpy pynput
```

**New dependency:** `pynput` for recording mode

### 2. Run
```bash
python osrs_bot.py
```

Or double-click `START.bat` on Windows.

### 3. Recording Setup (NEW!)
```
🎬 RECORDING MODE SETUP
============================================================
1. Select potion
2. Press Enter to start recording
3. Just click each item:
   - Bank booth
   - Deposit button
   - Herb in bank
   - Secondary in bank
   - First inventory slot
4. Done! No Enter between steps!

✅ Setup complete!
📁 Check overlay_preview.png to see click zones
```

---

## Dialogue Validation Explained

### What It Checks

**1. Dark Background**
```python
gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
avg_brightness = np.mean(gray)
is_dark = avg_brightness < 80  # OSRS dialogues are dark
```

**2. Text Present**
```python
edges = cv2.Canny(gray, 50, 150)
edge_density = np.sum(edges) / edges.size
has_text = edge_density > 0.05  # Text creates edges
```

**3. OSRS UI Colors**
```python
hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
# Brown color range (OSRS UI)
lower_brown = [10, 50, 50]
upper_brown = [30, 255, 200]
brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
has_ui = np.sum(brown_mask) > 1000
```

**Decision:**
```python
dialogue_present = (is_dark AND has_text) OR has_ui
```

### When It Runs

```
[MAKING POTIONS]
  Step 1: Click herb ✓
  Step 2: Click secondary ✓
  Step 3: Wait 1.5s for dialogue...
  
  [VALIDATE] Checking for makex dialogue...
  📸 Capturing center screen (400×300)
  🔍 Analyzing: brightness, edges, colors
  
  ✅ Dialogue check: dark=True, text=True, ui=True
  
  Step 4: Press Space ✓
```

### If Validation Fails

```
  [VALIDATE] Checking for makex dialogue...
  ❌ Dialogue check: dark=False, text=False, ui=False
  📸 Saved to: validation_checks/dialogue_makex_162547.png
  
  ⚠️  Make-X dialogue didn't appear - retrying...
  [Press ESC to clear]
  
  Step 1: Click herb... (attempt 2/3)
```

---

## Visual Overlay Examples

### What You'll See

**overlay_preview.png:**
```
┌──────────────────────────────────────┐
│                                      │
│     Bank Booth                       │
│     ┌─────────────┐                  │
│     │             │ ← Yellow square  │
│     │      +      │    (±15px)       │
│     │             │    Red crosshair │
│     └─────────────┘                  │
│                                      │
│     Herb in Bank                     │
│     ┌─────────────┐                  │
│     │      +      │                  │
│     └─────────────┘                  │
│                                      │
│     Secondary in Bank                │
│     ┌─────────────┐                  │
│     │      +      │                  │
│     └─────────────┘                  │
│                                      │
└──────────────────────────────────────┘
```

**What the overlay shows:**
- ✅ Center position (red crosshair)
- ✅ Click variance zone (yellow square)
- ✅ Maximum click boundaries
- ✅ Label for each position

**How to interpret:**
- If squares overlap → positions too close
- If square cuts off screen → position near edge
- If crosshair in wrong spot → redo setup

---

## One-Click Recording Details

### How It Works

**Traditional Setup:**
```python
# Old way
def capture():
    input("Press Enter...")  # User action
    time.sleep(3)            # Wait
    pos = pyautogui.position()
    # Capture...
    input("Correct? (y/n)")  # User confirmation
```

**Recording Mode:**
```python
# New way
def on_click(x, y, button, pressed):
    if recording and pressed and button == mouse.Button.left:
        # Auto-capture immediately!
        capture_position(x, y)
        advance_to_next_step()

# Start listener
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()
```

**Benefits:**
- No waiting
- No confirmation needed
- Natural workflow
- Faster setup
- Real-time capture

### Recording Session Example

```
🎬 STARTING RECORDING
============================================================
⚠️  Just CLICK each item as you normally would.
⚠️  Bot will automatically capture each click.
⚠️  No need to press Enter between steps!

👉 Press Enter to start recording...

============================================================
📍 FIRST STEP: BANK
============================================================
🏦 Click the bank booth/chest to record its position.

  📍 Captured: bank at (1127, 384)

============================================================
📍 NEXT: DEPOSIT
============================================================
📤 Open the bank, then click "Deposit Inventory" button.

  📍 Captured: deposit at (1456, 782)

============================================================
📍 NEXT: HERB
============================================================
🌿 Click 'Guam leaf' in your bank.

  📍 Captured: herb at (1234, 567)

[... continues automatically ...]

✅ Recording complete!
```

---

## Performance

**Expected rates** (with dialogue validation):

| Potion | XP/hour | Potions/hour | Notes |
|--------|---------|--------------|-------|
| Attack | ~30k | ~1,200 | Slightly slower (validation) |
| Strength | ~40k | ~800 | |
| Prayer | ~68k | ~780 | |
| Super attack | ~78k | ~780 | |
| Super strength | ~93k | ~745 | |
| Ranging | ~122k | ~750 | |

**Performance impact:**
- Dialogue check: +1.5s per potion cycle
- Validation time: ~0.5s per check
- Retry overhead: Only on failures
- Overall: ~10% slower but much safer

**Trade-off:**
- v3: Fast but risky (misclicks waste inventory)
- v4: Slightly slower but catches errors

---

## Files

```
osrs-herblore-bot/
├── osrs_bot.py              ← Main bot (32KB, v4)
├── START.bat                ← Windows launcher
├── README.md                ← This file
├── POTION_RECIPES.md        ← Recipe reference
├── bot_config.json          ← Auto-generated
├── overlay_preview.png      ← Auto-generated (visual overlay)
├── templates/               ← Auto-generated
│   ├── bank.png
│   ├── herb.png
│   ├── secondary.png
│   ├── deposit.png
│   └── inv_first.png
└── validation_checks/       ← Auto-generated
    ├── bank_160523.png
    ├── herb_160526.png
    ├── secondary_160529.png
    └── dialogue_makex_162547.png  ← NEW!
```

---

## Troubleshooting

### "Dialogue validation keeps failing"
**Cause:** Make-X interface looks different
**Check:** `validation_checks/dialogue_makex_*.png`
**Fix:** 
- Ensure you're using standard RuneLite
- Check if dialogue actually appeared
- Lower threshold if needed (edit code)

### "Recording mode captured wrong click"
**Cause:** Accidentally clicked during recording
**Fix:** 
- Delete `bot_config.json`
- Delete `templates/` folder
- Run setup again

### "Overlay shows overlapping zones"
**Cause:** Positions too close together
**Fix:**
- Move items further apart in bank
- Redo setup with better spacing

### "Bot still clicking wrong secondary"
**Benefit of v4:** Now it will detect and retry!
**Check:** `validation_checks/dialogue_*.png` to see what happened

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

**v4 Improvements:**
- ✅ Dialogue validation (more human-like)
- ✅ Catches errors (prevents bot-like behavior)
- ✅ Variable delays
- ✅ Natural setup process

---

## Changelog

### v4.0 (2026-03-07)
- ✅ Dialogue box validation (Make-X detection)
- ✅ Visual overlay preview (overlay_preview.png)
- ✅ One-click recording mode (pynput listeners)
- ✅ Adaptive validation threshold (learns from variance)
- ✅ Enhanced potion-making instructions (5 steps)
- ✅ Better error messages
- ✅ Improved failsafe (catches failed secondary clicks)

### v3.0 (2026-03-07)
- ✅ Position variance
- ✅ Enhanced smooth movement
- ✅ Human-like behavior
- ✅ Better setup wizard

### v2.0 (2026-03-07)
- ✅ Misclick detection
- ✅ Visual validation
- ✅ Single-click withdraws

### v1.0 (2026-03-07)
- Initial release

---

## Resources

- **OSRS Wiki:** https://oldschool.runescape.wiki/w/Herblore
- **Recipes:** See POTION_RECIPES.md
- **GitHub:** https://github.com/sergenfloppy-lgtm/osrs-herblore-bot

---

**Educational purposes only. Use at your own risk.**

**Version:** 4.0  
**Last Updated:** 2026-03-07  
**Safety Rating:** ⭐⭐⭐⭐⭐ (Dialogue validation adds safety)
