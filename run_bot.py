#!/usr/bin/env python3
"""Safe wrapper for main.py that checks dependencies first."""
import sys
import os

print("""
╔═══════════════════════════════════════════════════════════╗
║          OSRS Herblore Bot - Dependency Check             ║
╚═══════════════════════════════════════════════════════════╝
""")

# Check dependencies first
print("[1/3] Checking Python dependencies...")

missing = []
dependencies = {
    'mss': 'pip install mss',
    'cv2': 'pip install opencv-python',
    'numpy': 'pip install numpy',
    'PIL': 'pip install pillow',
    'pyautogui': 'pip install pyautogui',
    'scipy': 'pip install scipy',
}

for module, install_cmd in dependencies.items():
    try:
        __import__(module)
    except ImportError:
        missing.append((module, install_cmd))

if missing:
    print("\n❌ MISSING DEPENDENCIES DETECTED!\n")
    print("The following packages are required but not installed:\n")
    for module, install_cmd in missing:
        print(f"  • {module:<15} → {install_cmd}")
    
    print("\n" + "="*60)
    print("⚠️  THIS BOT CANNOT RUN ON THIS SERVER")
    print("="*60)
    print("""
Reasons:
  1. This server has no pip (Python package manager)
  2. This server has no GUI/display
  3. OSRS is not installed here
  4. Can't control your local mouse/keyboard remotely

SOLUTION: Run this bot on your gaming computer!

Steps:
  1. Download from: https://github.com/sergenfloppy-lgtm/osrs-herblore-bot
  2. Install Python 3.11+ on your PC
  3. Run: pip install -r requirements.txt
  4. Run: python main.py
  5. Follow the setup wizard

The bot needs to run where you play OSRS!
    """)
    sys.exit(1)

print("✅ All dependencies installed!\n")

# Check for display
print("[2/3] Checking for display...")
if not os.environ.get('DISPLAY'):
    print("⚠️  WARNING: No DISPLAY environment variable")
    print("   The bot needs a GUI to capture the game screen.")
    print("   This might fail if you're running on a headless server.\n")

print("[3/3] Starting bot...")
print("-" * 60 + "\n")

# Import and run main
try:
    from main import main
    main()
except KeyboardInterrupt:
    print("\n\n[BOT] Stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"\n\n❌ BOT CRASHED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
