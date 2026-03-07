#!/usr/bin/env python3
"""
OSRS Herblore Bot - Simple Click Setup
Click on items directly - no F8 needed!
"""
import time
import random
import json
import math
from datetime import datetime
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Bot - Simple Click Setup                          ║
║   Just click on items when asked!                        ║
╚═══════════════════════════════════════════════════════════╝
""")

# Dependencies
try:
    import pyautogui
    import mss
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw
    print("✅ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    input("Press Enter to exit...")
    exit(1)

# Config
pyautogui.FAILSAFE = True


class SimpleSetup:
    """Simple click-based setup."""
    
    def __init__(self):
        self.positions = {}
        self.sct = mss.mss()
    
    def wait_for_click(self, step_name, instruction):
        """Wait for user to click."""
        print(f"\n{'='*60}")
        print(f"STEP: {step_name}")
        print(f"{'='*60}")
        print(instruction)
        print("\n👉 Click on the item/position when ready")
        print("👉 Bot will capture your click position")
        print()
        
        input("Press Enter, then click...")
        
        print("Waiting for click (move mouse and click)...")
        time.sleep(1)
        
        # Wait for click
        initial_pos = pyautogui.position()
        print("Move your mouse to the position and click...")
        
        # Simple approach: wait 3 seconds for user to click
        time.sleep(3)
        
        # Get final position
        pos = pyautogui.position()
        self.positions[step_name] = (pos.x, pos.y)
        
        print(f"✅ Saved: {step_name} at ({pos.x}, {pos.y})")
        
        # Visual confirmation - move mouse there
        pyautogui.moveTo(pos.x, pos.y)
        time.sleep(0.5)
        
        confirm = input("Is this correct? (y/n): ").strip().lower()
        if confirm != 'y':
            return self.wait_for_click(step_name, instruction)
        
        return pos
    
    def run_setup(self):
        """Run simple setup."""
        print("\n" + "="*60)
        print("SIMPLE SETUP - Click on items")
        print("="*60)
        print("\nYou'll click on 5 things:")
        print("  1. Bank booth")
        print("  2. Deposit inventory button (in bank)")
        print("  3. Herb in bank")
        print("  4. Vial in bank")
        print("  5. First inventory slot")
        print()
        input("Press Enter to start...")
        
        # 1. Bank
        self.wait_for_click(
            "bank",
            "BANK BOOTH:\n"
            "Position your mouse over the bank booth/chest.\n"
            "(The thing you click to open the bank)"
        )
        
        # Open bank
        print("\n📋 Now OPEN the bank")
        input("Press Enter once bank is open...")
        
        # 2. Deposit button
        self.wait_for_click(
            "deposit_button",
            "DEPOSIT INVENTORY BUTTON:\n"
            "Position your mouse over the 'Deposit Inventory' button.\n"
            "(Usually bottom-right of bank)"
        )
        
        # 3. Herb
        print("\n📋 Find your herb in the bank")
        
        self.wait_for_click(
            "herb_bank",
            "HERB IN BANK:\n"
            "Position your mouse over your herb in the bank.\n"
            "(We'll right-click and withdraw-all)"
        )
        
        # 4. Vials
        self.wait_for_click(
            "vial_bank",
            "VIALS IN BANK:\n"
            "Position your mouse over 'Vial of water' in the bank."
        )
        
        # Close bank
        print("\n📋 Close the bank (ESC)")
        input("Press Enter once closed...")
        
        # 5. First inv slot
        self.wait_for_click(
            "inv_first",
            "FIRST INVENTORY SLOT:\n"
            "Position your mouse over the FIRST slot in your inventory.\n"
            "(Top-left)"
        )
        
        # Calculate grid
        print("\n[CALCULATING] Other inventory slots...")
        self._calculate_inventory()
        
        # Save
        self._save()
        
        print("\n✅ Setup complete!")
        return True
    
    def _calculate_inventory(self):
        """Calculate inventory grid."""
        x, y = self.positions['inv_first']
        
        slots = []
        for row in range(7):
            for col in range(4):
                slot_x = x + (col * 42)
                slot_y = y + (row * 36)
                slots.append((slot_x, slot_y))
        
        self.positions['inventory_slots'] = slots
        print(f"✅ Calculated {len(slots)} slots")
    
    def _save(self):
        """Save setup."""
        with open('simple_setup.json', 'w') as f:
            json.dump(self.positions, f, indent=2)
        print("📁 Saved to simple_setup.json")
    
    def load(self):
        """Load setup."""
        if not Path('simple_setup.json').exists():
            return False
        
        try:
            with open('simple_setup.json', 'r') as f:
                self.positions = json.load(f)
            print("✅ Loaded saved setup")
            return True
        except Exception as e:
            print(f"⚠️  Failed to load: {e}")
            return False


class BezierMovement:
    """Smooth movements."""
    
    @staticmethod
    def move_click(x, y):
        """Move and click."""
        start = pyautogui.position()
        x += random.randint(-3, 3)
        y += random.randint(-3, 3)
        
        distance = math.sqrt((x - start[0])**2 + (y - start[1])**2)
        num_points = max(10, int(distance / 30))
        
        ctrl1_x = start[0] + (x - start[0]) * 0.25 + random.randint(-20, 20)
        ctrl1_y = start[1] + (y - start[1]) * 0.25 + random.randint(-20, 20)
        ctrl2_x = start[0] + (x - start[0]) * 0.75 + random.randint(-20, 20)
        ctrl2_y = start[1] + (y - start[1]) * 0.75 + random.randint(-20, 20)
        
        for i in range(num_points + 1):
            t = i / num_points
            px = ((1-t)**3 * start[0] + 3*(1-t)**2*t * ctrl1_x + 
                  3*(1-t)*t**2 * ctrl2_x + t**3 * x)
            py = ((1-t)**3 * start[1] + 3*(1-t)**2*t * ctrl1_y + 
                  3*(1-t)*t**2 * ctrl2_y + t**3 * y)
            
            pyautogui.moveTo(int(px), int(py))
            time.sleep(random.uniform(0.001, 0.003))
        
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.click()


class Bot:
    """Simple bot."""
    
    def __init__(self, setup):
        self.setup = setup
        self.potions_made = 0
        self.running = True
    
    def start(self):
        """Start."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print("="*60)
        print("\n⚠️  Move mouse to corner to stop")
        
        input("Press Enter to start...")
        
        start_time = datetime.now()
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                self._bank()
                self._make_potions()
                
                self.potions_made += 14
                elapsed = (datetime.now() - start_time).total_seconds()
                
                print(f"\n📊 Potions: {self.potions_made}")
                print(f"📊 Runtime: {int(elapsed)}s")
                
                delay = random.uniform(3, 6)
                print(f"\n⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n[BOT] Stopped")
        except pyautogui.FailSafeException:
            print("\n[BOT] FAILSAFE")
        finally:
            print("\n" + "="*60)
            print("STOPPED")
            print("="*60)
    
    def _bank(self):
        """Bank."""
        print("[BANKING]")
        
        # Bank
        print("  Opening bank...")
        x, y = self.setup.positions['bank']
        BezierMovement.move_click(x, y)
        time.sleep(random.uniform(1.5, 2.0))
        
        # Deposit
        print("  Depositing...")
        x, y = self.setup.positions['deposit_button']
        BezierMovement.move_click(x, y)
        time.sleep(random.uniform(0.6, 0.9))
        
        # Herbs
        print("  Withdrawing herbs...")
        x, y = self.setup.positions['herb_bank']
        BezierMovement.move_click(x, y)
        time.sleep(0.3)
        pyautogui.click(button='right')
        time.sleep(0.3)
        pyautogui.moveRel(0, 60)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 0.9))
        
        # Vials
        print("  Withdrawing vials...")
        x, y = self.setup.positions['vial_bank']
        BezierMovement.move_click(x, y)
        time.sleep(0.3)
        pyautogui.click(button='right')
        time.sleep(0.3)
        pyautogui.moveRel(0, 60)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 0.9))
        
        # Close
        print("  Closing...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print("  ✅ Done")
    
    def _make_potions(self):
        """Make."""
        print("\n[MAKING]")
        
        slots = self.setup.positions['inventory_slots']
        
        # Herb
        print("  Clicking herb...")
        x, y = slots[0]
        BezierMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.5))
        
        # Vial
        print("  Clicking vial...")
        x, y = slots[14]
        BezierMovement.move_click(x, y)
        time.sleep(random.uniform(0.8, 1.2))
        
        # Space
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Wait
        print("  Waiting 28s...")
        time.sleep(28)
        
        print("  ✅ Done")


def main():
    """Main."""
    setup = SimpleSetup()
    
    # Load or setup
    if setup.load():
        reuse = input("\nReuse saved setup? (y/n): ").strip().lower()
        if reuse != 'y':
            setup.run_setup()
    else:
        setup.run_setup()
    
    # Start
    bot = Bot(setup)
    bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter...")
