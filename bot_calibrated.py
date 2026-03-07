#!/usr/bin/env python3
"""
OSRS Herblore Bot - Calibrated Version
Shows you where it will click and lets you adjust positions
"""
import time
import random
import json
import math
from datetime import datetime
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Bot - Calibrated Version                          ║
║   Manual position setup with visual feedback             ║
╚═══════════════════════════════════════════════════════════╝
""")

# Check dependencies
try:
    import pyautogui
    import mss
    from PIL import Image, ImageDraw
    print("✅ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    input("Press Enter to exit...")
    exit(1)

# Configure
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


def show_click_position(x, y, label="Position"):
    """Show where the bot will click with a visual indicator."""
    print(f"\n[VISUAL] Showing {label} at ({x}, {y})")
    print("The mouse will move there for 2 seconds so you can see it.")
    
    # Move to position
    pyautogui.moveTo(x, y, duration=0.5)
    time.sleep(2)
    
    # Move away
    pyautogui.moveRel(50, 50, duration=0.3)


def calibrate_position(prompt):
    """Let user define a position by moving mouse."""
    print(f"\n{prompt}")
    input("Move your mouse to the position and press Enter...")
    pos = pyautogui.position()
    print(f"✅ Position set: {pos}")
    
    # Show it back
    show_click_position(pos[0], pos[1], "Your position")
    
    confirm = input("Is this correct? (y/n): ").strip().lower()
    if confirm == 'y':
        return pos
    else:
        print("Let's try again...")
        return calibrate_position(prompt)


def bezier_move_click(start, end, click_offset=3):
    """Move using Bezier curve and click."""
    x1, y1 = start
    x2, y2 = end
    
    # Add click offset
    x2 += random.randint(-click_offset, click_offset)
    y2 += random.randint(-click_offset, click_offset)
    
    # Generate curve points
    ctrl1_x = x1 + (x2 - x1) * 0.3 + random.randint(-20, 20)
    ctrl1_y = y1 + (y2 - y1) * 0.3 + random.randint(-20, 20)
    ctrl2_x = x1 + (x2 - x1) * 0.7 + random.randint(-20, 20)
    ctrl2_y = y1 + (y2 - y1) * 0.7 + random.randint(-20, 20)
    
    points = []
    for i in range(16):
        t = i / 15
        x = ((1-t)**3 * x1 + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * x2)
        y = ((1-t)**3 * y1 + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * y2)
        points.append((int(x), int(y)))
    
    # Move along curve
    for point in points:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(random.uniform(0.001, 0.003))
    
    # Click
    time.sleep(random.uniform(0.05, 0.15))
    pyautogui.click()


class CalibratedBot:
    """Bot with manual calibration."""
    
    def __init__(self, potion_name):
        self.potion_name = potion_name
        self.potions_made = 0
        self.running = True
        
        # Positions (to be calibrated)
        self.bank_pos = None
        self.deposit_all_button = None
        self.herb_bank_slot = None
        self.vial_bank_slot = None
        self.inventory_first_slot = None
        self.inventory_slots = []
        
        # Load potion data
        with open('data/potions.json', 'r') as f:
            data = json.load(f)
            potions = {p['name']: p for p in data['potions']}
            self.potion = potions[potion_name]
        
        print(f"\n[BOT] Configured for: {self.potion['name']}")
        print(f"[BOT] Herb: {self.potion['herb']}")
        print(f"[BOT] Secondary: {self.potion['secondary']}")
    
    def calibrate(self):
        """Calibrate all positions."""
        print("\n" + "="*60)
        print("CALIBRATION - Define All Positions")
        print("="*60)
        print("\nWe'll go through each position one by one.")
        print("The bot will show you where it will click.")
        print()
        
        # 1. Bank booth
        print("\n[STEP 1/5] Bank Booth")
        self.bank_pos = calibrate_position(
            "Click on the bank booth/chest to open it.\n"
            "Move your mouse to the CENTER of the bank booth."
        )
        
        # 2. Deposit all button
        print("\n[STEP 2/5] Deposit All Button")
        print("Open your bank interface in OSRS (click the bank).")
        input("Press Enter once bank is open...")
        self.deposit_all_button = calibrate_position(
            "Move your mouse to the 'Deposit Inventory' button.\n"
            "(Usually at bottom-right of bank interface)"
        )
        
        # 3. Herb in bank
        print("\n[STEP 3/5] Herb in Bank")
        print(f"Find your {self.potion['herb']} in the bank.")
        self.herb_bank_slot = calibrate_position(
            f"Move your mouse to the {self.potion['herb']} in your bank.\n"
            "(We'll right-click and withdraw-all)"
        )
        
        # 4. Vials in bank
        print("\n[STEP 4/5] Vials in Bank")
        print("Find 'Vial of water' in your bank.")
        self.vial_bank_slot = calibrate_position(
            "Move your mouse to 'Vial of water' in your bank."
        )
        
        # Close bank
        print("\nClosing bank...")
        pyautogui.press('esc')
        time.sleep(1)
        
        # 5. Inventory slots
        print("\n[STEP 5/5] Inventory Slots")
        self.inventory_first_slot = calibrate_position(
            "Move your mouse to the FIRST inventory slot.\n"
            "(Top-left of your inventory)"
        )
        
        # Calculate other slots
        print("\n[CALCULATING] Other inventory slots...")
        base_x, base_y = self.inventory_first_slot
        self.inventory_slots = []
        for row in range(7):
            for col in range(4):
                x = base_x + (col * 42)
                y = base_y + (row * 36)
                self.inventory_slots.append((x, y))
        
        print(f"✅ Calculated {len(self.inventory_slots)} slots")
        
        # Show some slots
        print("\n[VERIFY] Showing inventory slots...")
        for i in [0, 13, 27]:  # First, middle, last
            print(f"Slot {i+1}:")
            show_click_position(self.inventory_slots[i][0], self.inventory_slots[i][1], f"Slot {i+1}")
        
        confirm = input("\nDo the inventory slots look correct? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Let's recalibrate inventory...")
            return self.calibrate()
        
        print("\n✅ Calibration complete!")
        
        # Save calibration
        self._save_calibration()
    
    def _save_calibration(self):
        """Save calibration to file."""
        data = {
            'bank_pos': self.bank_pos,
            'deposit_all_button': self.deposit_all_button,
            'herb_bank_slot': self.herb_bank_slot,
            'vial_bank_slot': self.vial_bank_slot,
            'inventory_first_slot': self.inventory_first_slot,
        }
        
        Path('calibration.json').write_text(json.dumps(data, indent=2))
        print("\n[SAVED] Calibration saved to calibration.json")
        print("You can reuse this next time!")
    
    def _load_calibration(self):
        """Load calibration from file."""
        if not Path('calibration.json').exists():
            return False
        
        try:
            data = json.loads(Path('calibration.json').read_text())
            self.bank_pos = tuple(data['bank_pos'])
            self.deposit_all_button = tuple(data['deposit_all_button'])
            self.herb_bank_slot = tuple(data['herb_bank_slot'])
            self.vial_bank_slot = tuple(data['vial_bank_slot'])
            self.inventory_first_slot = tuple(data['inventory_first_slot'])
            
            # Calculate inventory slots
            base_x, base_y = self.inventory_first_slot
            self.inventory_slots = []
            for row in range(7):
                for col in range(4):
                    x = base_x + (col * 42)
                    y = base_y + (row * 36)
                    self.inventory_slots.append((x, y))
            
            print("✅ Loaded calibration from file")
            return True
        except Exception as e:
            print(f"⚠️  Failed to load calibration: {e}")
            return False
    
    def start(self):
        """Start the bot."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print("="*60)
        print("\n⚠️  Bot will control your mouse!")
        print("⚠️  Move to TOP-LEFT corner to stop")
        print("⚠️  Or press Ctrl+C\n")
        
        print("MAKE SURE:")
        print("  ✅ Standing at Varrock East Bank")
        print("  ✅ Bank has herbs and vials")
        print("  ✅ Inventory is empty or ready")
        print()
        
        input("Press Enter to start...")
        
        start_time = datetime.now()
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                # Banking
                self._do_banking()
                
                # Make potions
                self._make_potions()
                
                # Stats
                self.potions_made += 14
                elapsed = (datetime.now() - start_time).total_seconds()
                xp = self.potions_made * self.potion['xp']
                xp_per_hour = (xp / elapsed * 3600) if elapsed > 0 else 0
                
                print(f"\n📊 Stats:")
                print(f"  Potions: {self.potions_made}")
                print(f"  XP: {xp:,.0f}")
                print(f"  XP/hr: {xp_per_hour:,.0f}")
                print(f"  Runtime: {int(elapsed)}s")
                
                # Delay
                delay = random.uniform(3, 6)
                print(f"\n⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\n[BOT] Stopped by user")
        except pyautogui.FailSafeException:
            print("\n\n[BOT] FAILSAFE triggered")
        finally:
            print("\n" + "="*60)
            print("BOT STOPPED")
            print("="*60)
    
    def _do_banking(self):
        """Banking with actual clicks."""
        print("[BANKING]")
        
        current = pyautogui.position()
        
        # Click bank
        print("  Opening bank...")
        bezier_move_click(current, self.bank_pos)
        time.sleep(random.uniform(1.5, 2.0))
        
        # Deposit all
        current = pyautogui.position()
        print("  Depositing inventory...")
        bezier_move_click(current, self.deposit_all_button)
        time.sleep(random.uniform(0.6, 0.9))
        
        # Withdraw herbs
        current = pyautogui.position()
        print(f"  Withdrawing {self.potion['herb']}...")
        bezier_move_click(current, self.herb_bank_slot)
        time.sleep(0.3)
        # Right-click menu: Withdraw-All is usually 3rd option
        pyautogui.click(button='right')
        time.sleep(0.2)
        pyautogui.moveRel(0, 60)  # Move down to "Withdraw-All"
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.5, 0.8))
        
        # Withdraw vials
        current = pyautogui.position()
        print("  Withdrawing vials...")
        bezier_move_click(current, self.vial_bank_slot)
        time.sleep(0.3)
        pyautogui.click(button='right')
        time.sleep(0.2)
        pyautogui.moveRel(0, 60)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.5, 0.8))
        
        # Close bank
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print("  ✅ Banking complete")
    
    def _make_potions(self):
        """Make potions."""
        print("\n[MAKING POTIONS]")
        
        current = pyautogui.position()
        
        # Click first herb
        herb_slot = self.inventory_slots[0]
        print("  Clicking herb...")
        bezier_move_click(current, herb_slot)
        time.sleep(random.uniform(0.3, 0.5))
        
        # Click first vial (slot 15)
        current = pyautogui.position()
        vial_slot = self.inventory_slots[14]
        print("  Clicking vial...")
        bezier_move_click(current, vial_slot)
        time.sleep(random.uniform(0.8, 1.2))
        
        # Press space
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Wait
        wait_time = 14 * 2
        print(f"  Waiting {wait_time}s...")
        time.sleep(wait_time)
        
        print("  ✅ Potions made")


def main():
    """Main entry point."""
    # Load potions
    with open('data/potions.json', 'r') as f:
        data = json.load(f)
    
    print("Available Potions:")
    print("-" * 60)
    for i, p in enumerate(data['potions'], 1):
        print(f"{i:2d}. {p['name']:<20} (Lvl {p['level']:2d}, {p['xp']:5.1f} XP)")
    print("-" * 60)
    
    # Select potion
    while True:
        try:
            choice = int(input("\nSelect potion (1-11): ").strip())
            if 1 <= choice <= len(data['potions']):
                potion = data['potions'][choice - 1]
                break
        except:
            pass
    
    print(f"\n✅ Selected: {potion['name']}\n")
    
    # Create bot
    bot = CalibratedBot(potion['name'])
    
    # Try to load existing calibration
    if bot._load_calibration():
        reuse = input("\nReuse saved calibration? (y/n): ").strip().lower()
        if reuse != 'y':
            bot.calibrate()
    else:
        bot.calibrate()
    
    # Start
    bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
