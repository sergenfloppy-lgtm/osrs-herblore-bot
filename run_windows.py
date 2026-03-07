#!/usr/bin/env python3
"""
Windows-friendly launcher that keeps the window open
"""
import sys
import os

print("=" * 70)
print("OSRS Bot - Windows Launcher")
print("=" * 70)
print()

# Check we're in the right directory
print("[1/5] Checking files...")
if not os.path.exists('data/potions.json'):
    print("❌ ERROR: data/potions.json not found!")
    print("   Make sure you're running from the bot folder.")
    print()
    input("Press Enter to close...")
    sys.exit(1)
print("✅ Files found")
print()

# Check Python version
print("[2/5] Checking Python version...")
version = sys.version_info
print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
print()

# Check dependencies
print("[3/5] Checking dependencies...")
missing = []
deps = {
    'mss': 'Screen capture',
    'pyautogui': 'Mouse/keyboard control',
    'numpy': 'Arrays',
    'PIL': 'Image processing',
}

for module, desc in deps.items():
    try:
        __import__(module)
        print(f"✅ {module:<15} - {desc}")
    except ImportError:
        print(f"❌ {module:<15} - {desc} - NOT INSTALLED")
        missing.append(module)

print()

if missing:
    print("=" * 70)
    print("⚠️  MISSING DEPENDENCIES")
    print("=" * 70)
    print()
    print("To install missing packages, run this command:")
    print()
    if 'PIL' in missing:
        missing[missing.index('PIL')] = 'pillow'
    print(f"    pip install {' '.join(missing)}")
    print()
    print("Or install everything:")
    print("    pip install -r requirements.txt")
    print()
    print("=" * 70)
    print()
    response = input("Continue in DEMO MODE anyway? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        input("Press Enter to close...")
        sys.exit(0)
    print()

# Run the bot
print("[4/5] Starting bot...")
print()

try:
    # Import and run
    import bot_simple
    bot_simple.main()
    
except FileNotFoundError as e:
    print()
    print("=" * 70)
    print("❌ FILE NOT FOUND ERROR")
    print("=" * 70)
    print(f"Error: {e}")
    print()
    print("Make sure you're in the osrs-herblore-bot folder!")
    print()
    
except KeyboardInterrupt:
    print()
    print("Stopped by user (Ctrl+C)")
    
except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERROR OCCURRED")
    print("=" * 70)
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print()
    print("Full error details:")
    import traceback
    traceback.print_exc()
    print()

# Keep window open
print()
print("=" * 70)
input("Press Enter to close this window...")
