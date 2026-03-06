## OSRS Herblore Bot

An advanced, educational bot for training Herblore in Old School RuneScape with anti-detection features.

⚠️ **DISCLAIMER**: Botting violates Jagex's Terms of Service. This project is for **educational and research purposes only**. Use at your own risk. The authors are not responsible for any account bans.

## Features

### Core Functionality
- ✅ **Automated Potion Making** - Supports 11 different potions (Attack → Saradomin brew)
- ✅ **Bank Integration** - Auto-withdraw ingredients, deposit finished potions
- ✅ **Progressive Training** - Automatically levels from low to high tier potions
- ✅ **Smart Detection** - Computer vision for interface detection
- ✅ **Statistics Tracking** - XP/hr, potions/hr, runtime

### Anti-Detection (Anti-Ban)
- ✅ **Humanized Mouse Movement** - Bezier curves with random control points
- ✅ **Random Delays** - Gaussian distribution (50-300ms)
- ✅ **Misclicks** - 5% chance to slightly miss target first
- ✅ **Random Breaks** - Every 15-45 minutes, 1-3 minute breaks
- ✅ **Session Limits** - Auto-logout after 4-6 hours
- ✅ **Activity Variation** - Random camera movements, skill checks

### Safety
- Combat detection → instant logout
- Player proximity detection
- Random event handling (placeholder)
- Graceful error handling

## Tech Stack

- **Python 3.12**
- **OpenCV** - Computer vision / template matching
- **mss** - Fast screen capture
- **PyAutoGUI** - Mouse/keyboard control
- **Pytesseract** - OCR (optional, for text reading)
- **NumPy / SciPy** - Mathematical operations

## Installation

### Prerequisites
- Python 3.11+
- Old School RuneScape (obviously)
- Tesseract OCR (optional, for advanced features)

### Setup

```bash
# Clone the repo
git clone https://github.com/sergenfloppy-lgtm/osrs-herblore-bot.git
cd osrs-herblore-bot

# Install dependencies
pip install -r requirements.txt

# (Optional) Install Tesseract for OCR
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Usage

### Quick Start

```bash
python main.py
```

The bot will run an interactive setup wizard:
1. Define your OSRS game window region (move mouse to corners)
2. Select which potion to make
3. Press Enter to start

### List Available Potions

```bash
python main.py --list
```

### Requirements Before Starting

1. **Be logged into OSRS**
2. **Stand next to a bank** (or bank chest)
3. **Bank contains:**
   - Grimy or clean herbs (14+)
   - Vials of water (14+)
4. **Fixed or resizable classic mode** (not resizable modern)

### Example Session

```
[BOT] Starting Herblore bot for Prayer potion
[BOT] Required: Ranarr weed + Snape grass
[BOT] Banking...
[BOT] Withdrawing Ranarr weed...
[BOT] Withdrawing vials of water...
[BOT] Making potions...
[BOT] Make-X interface detected
[BOT] Waiting 35s for completion...

==================================================
[STATS] Runtime: 5m 23s
[STATS] Potions made: 56
[STATS] XP gained: 4,900
[STATS] XP/hr: 54,600
[STATS] Potions/hr: 624.0
[ANTIBAN] Actions: 12
[ANTIBAN] Next break: 847s
==================================================
```

## Project Structure

```
osrs-herblore-bot/
├── src/
│   ├── bot/
│   │   ├── herblore.py      # Main bot logic
│   │   ├── banking.py       # Bank interactions
│   │   ├── detection.py     # Computer vision
│   │   └── antiban.py       # Anti-detection
│   ├── utils/
│   │   ├── mouse.py         # Humanized movements
│   │   ├── keyboard.py
│   │   └── screen.py        # Screen capture
│   └── config.py            # Configuration
├── data/
│   ├── templates/           # UI element images (for template matching)
│   └── potions.json         # Potion data (herbs, secondaries, XP, levels)
├── main.py                  # Entry point
├── requirements.txt
└── README.md
```

## Supported Potions

| Potion | Level | Herb | Secondary | XP |
|--------|-------|------|-----------|-----|
| Attack potion | 3 | Guam leaf | Eye of newt | 25 |
| Antipoison | 5 | Marrentill | Unicorn horn dust | 37.5 |
| Strength potion | 12 | Tarromin | Limpwurt root | 50 |
| Restore potion | 22 | Harralander | Red spiders' eggs | 62.5 |
| Prayer potion | 38 | Ranarr weed | Snape grass | 87.5 |
| Super attack | 45 | Irit leaf | Eye of newt | 100 |
| Super strength | 55 | Kwuarm | Limpwurt root | 125 |
| Super restore | 63 | Snapdragon | Red spiders' eggs | 142.5 |
| Super defence | 66 | Cadantine | White berries | 150 |
| Ranging potion | 72 | Dwarf weed | Wine of zamorak | 162.5 |
| Saradomin brew | 81 | Toadflax | Crushed nest | 180 |

## How It Works

### 1. Computer Vision Pipeline
- **Screen Capture**: Fast screenshot using `mss` library
- **Template Matching**: OpenCV compares game elements to pre-saved templates
- **Color Detection**: HSV color space for detecting bank interface, inventory slots
- **OCR**: Pytesseract reads text (for future enhancements)

### 2. State Machine
The bot operates as a finite state machine:

```
IDLE → CHECK_INVENTORY → 
  ↓ (empty)         ↓ (has items)
BANKING         MAKE_POTIONS
  ↓                   ↓
WITHDRAW_ITEMS → (loop back)
```

### 3. Anti-Detection
- **Mouse Movement**: Bezier curves with 2-3 random control points
- **Delays**: Gaussian distribution (μ=150ms, σ=50ms)
- **Misclicks**: 5% chance to click slightly off-target first
- **Breaks**: Random intervals (15-45 min), duration (1-3 min)
- **Session Limit**: 4-6 hours then auto-logout
- **Random Activities**: Camera rotations, skill tab checks

### 4. Banking Logic
1. Detect bank interface (color matching)
2. Deposit all finished potions
3. Withdraw 14 herbs
4. Withdraw 14 vials of water
5. Close bank

### 5. Potion Making
1. Click herb in inventory
2. Click vial of water
3. Detect "Make-X" interface
4. Press spacebar to start
5. Wait for completion (~35 seconds for 14 potions)

## Configuration

Edit `src/config.py` to customize:

```python
# Anti-ban settings
BREAK_FREQUENCY_MIN = 15  # minutes
BREAK_FREQUENCY_MAX = 45
BREAK_DURATION_MIN = 60   # seconds
BREAK_DURATION_MAX = 180
MAX_SESSION_HOURS = (4, 6)

# Mouse settings
MISCLICK_CHANCE = 0.05  # 5%

# Action delays
ACTION_DELAY_MEAN = 0.15  # seconds
ACTION_DELAY_STD = 0.05
```

## Limitations & Future Improvements

### Current Limitations
- Only supports potion making (not cleaning herbs)
- Requires manual positioning at bank
- No GUI dashboard yet (CLI only)
- Template images not included (users must capture their own)
- Simplified detection (may not work in all scenarios)

### Planned Features (v2.0)
- [ ] PyQt6 GUI dashboard
- [ ] Herb cleaning support
- [ ] Grand Exchange integration
- [ ] Multiple potion types in one session
- [ ] Profit calculator
- [ ] Better template matching with included templates
- [ ] Multi-account support
- [ ] Discord webhook notifications

## Safety Tips

1. **Don't bot on your main account** - Use a throwaway alt
2. **Start with short sessions** - 30 min to 1 hour initially
3. **Vary your botting times** - Don't bot same hours every day
4. **Take manual breaks** - Play legitimately between bot sessions
5. **Don't bot while AFK** - Monitor the bot occasionally
6. **Use a VPN** (optional) - If paranoid about IP flagging

## Troubleshooting

**Bot can't find game window**
- Make sure OSRS is visible on screen
- Use fixed mode or resizable classic (not modern)
- Re-run setup wizard to redefine region

**Bank detection failing**
- Stand directly next to banker/chest
- Make sure camera angle shows the bank clearly
- Check that game brightness isn't too dark/bright

**Potion making stuck**
- Ensure inventory has correct items
- Check that "Make-X" interface is appearing
- Try restarting the bot

## Contributing

PRs welcome! Areas for improvement:
- Better template matching
- More robust detection algorithms
- GUI dashboard (PyQt6)
- Additional potion types
- Performance optimizations

## License

MIT License - See LICENSE file

---

**Remember**: This is an educational project. Botting is against OSRS rules and can result in permanent bans. Use responsibly (or not at all).

**Built by Sergenfloppy** | 2026-03-06
