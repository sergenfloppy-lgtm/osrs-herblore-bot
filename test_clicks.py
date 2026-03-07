#!/usr/bin/env python3
"""Test if PyAutoGUI can actually click on Windows"""
import time

print("=" * 60)
print("PyAutoGUI Click Test")
print("=" * 60)
print()

try:
    import pyautogui
    print("✅ PyAutoGUI imported")
except ImportError:
    print("❌ PyAutoGUI not installed")
    input("Press Enter to exit...")
    exit(1)

print()
print("This test will:")
print("1. Show your current mouse position")
print("2. Move the mouse slightly")
print("3. Try to click")
print()
input("Press Enter to start test...")

# Test 1: Get position
print("\n[TEST 1] Getting mouse position...")
try:
    pos = pyautogui.position()
    print(f"✅ Current position: {pos}")
except Exception as e:
    print(f"❌ Failed: {e}")
    input("Press Enter to exit...")
    exit(1)

# Test 2: Move mouse
print("\n[TEST 2] Moving mouse 100 pixels right...")
try:
    current = pyautogui.position()
    new_x = current[0] + 100
    new_y = current[1]
    print(f"Moving from {current} to ({new_x}, {new_y})...")
    pyautogui.moveTo(new_x, new_y, duration=1)
    time.sleep(0.5)
    final_pos = pyautogui.position()
    print(f"✅ Mouse moved to: {final_pos}")
except Exception as e:
    print(f"❌ Failed: {e}")
    input("Press Enter to exit...")
    exit(1)

# Test 3: Click
print("\n[TEST 3] Testing click...")
print("Watch for the click to happen...")
try:
    time.sleep(1)
    pyautogui.click()
    print("✅ Click executed (did you see/hear it?)")
except Exception as e:
    print(f"❌ Failed: {e}")
    input("Press Enter to exit...")
    exit(1)

# Test 4: Failsafes
print("\n[TEST 4] Checking PyAutoGUI settings...")
print(f"Failsafe enabled: {pyautogui.FAILSAFE}")
print(f"Pause between actions: {pyautogui.PAUSE}s")
print()
print("Note: If FAILSAFE is True, moving mouse to top-left corner stops the bot")

print()
print("=" * 60)
print("All tests passed! PyAutoGUI is working.")
print("=" * 60)
print()
print("If the bot still doesn't click:")
print("1. Make sure OSRS is in focus (click on the game window)")
print("2. Try running PowerShell as Administrator")
print("3. Check Windows Security settings (might block automation)")
print()
input("Press Enter to exit...")
