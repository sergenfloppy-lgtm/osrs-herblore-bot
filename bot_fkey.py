#!/usr/bin/env python3
"""
OSRS Herblore Bot - F-Key Setup
Simple guided setup: move mouse, press F to mark positions
"""
import time
import random
import json
import math
from datetime import datetime
from pathlib import Path
from pynput import keyboard

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Herblore Bot - F-Key Setup                        ║
║   Move mouse → Press F → Position saved!                 ║
╚═══════════════════════════════════════════════════════════╝
""")

# Check dependencies
try:
    import pyautogui
    from PIL import Image
    print("✅ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Install: pip install pyautogui pillow pynput")
    input("Press Enter to exit...")
    exit(1)

# Configure
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


class FKeySetup:
    """Guided setup using F key."""
    
    def __init__(self):
        self.positions = {}
        self.current_step = None
        self.f_pressed = False
        self.listener = None
    
    def on_press(self, key):
        """Handle F key press."""
        try:
            if key.char == 'f' or key.char == 'F':
                self.f_pressed = True
        except AttributeError:
            pass
    
    def wait_for_f(self, step_name, instruction):
        """Wait for user to press F."""
        print(f"\n{'='*60}")
        print(f"STEP: {step_name}")
        print(f"{'='*60}")
        print(instruction)
        print("\n👉 Move your mouse to the position")
        print("👉 Press F when ready")
        print()
        
        self.f_pressed = False
        
        # Start listening for F key
        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
        
        # Wait for F press
        while not self.f_pressed:
            time.sleep(0.1)
        
        # Get mouse position
        pos = pyautogui.position()
        self.positions[step_name] = (pos.x, pos.y)
        
        print(f"✅ Saved: {step_name} at ({pos.x}, {pos.y})")
        
        # Brief pause
        time.sleep(0.5)
        return pos
    
    def run_setup(self):
        """Run the full setup process."""
        print("\n" + "="*60)
        print("GUIDED SETUP - Press F at each step")
        print("="*60)
        print("\nWe'll set up 5 positions:")
        print("  1. Bank booth/chest")
        print("  2. Deposit inventory button")
        print("  3. Herb in bank")
        print("  4. Vials in bank")
        print("  5. First inventory slot")
        print()
        input("Press Enter to start setup...")
        
        # 1. Bank
        self.wait_for_f(
            "bank",
            "BANK BOOTH:\n"
            "Move your mouse to the CENTER of the bank booth or chest.\n"
            "(The thing you click to open the bank)"
        )
        
        # Open bank for next steps
        print("\n📋 Now OPEN your bank (click it once)")
        input("Press Enter once bank is open...")
        
        # 2. Deposit button
        self.wait_for_f(
            "deposit_button",
            "DEPOSIT INVENTORY BUTTON:\n"
            "Move your mouse to the 'Deposit Inventory' button.\n"
            "(Usually bottom-right of bank interface)"
        )
        
        # 3. Herb
        print("\n📋 Find your herb in the bank")
        herb_name = input("What herb are you using? (e.g., Ranarr weed): ").strip()
        self.positions['herb_name'] = herb_name
        
        self.wait_for_f(
            "herb_slot",
            f"HERB IN BANK:\n"
            f"Move your mouse to the {herb_name} in your bank.\n"
            "(We'll right-click and withdraw-all)"
        )
        
        # 4. Vials
        self.wait_for_f(
            "vial_slot",
            "VIALS IN BANK:\n"
            "Move your mouse to 'Vial of water' in your bank."
        )
        
        # Close bank
        print("\n📋 Close the bank (press ESC or click X)")
        input("Press Enter once bank is closed...")
        
        # 5. Inventory first slot
        self.wait_for_f(
            "inv_first_slot",
            "FIRST INVENTORY SLOT:\n"
            "Move your mouse to the FIRST inventory slot.\n"
            "(Top-left of your inventory)"
        )
        
        # Calculate other inventory slots
        print("\n[CALCULATING] Other 27 inventory slots...")
        self._calculate_inventory()
        
        # Save setup
        self._save_setup()
        
        print("\n✅ Setup complete!")
        print("✅ Saved to setup.json")
        
        # Stop listener
        if self.listener:
            self.listener.stop()
        
        return True
    
    def _calculate_inventory(self):
        """Calculate all 28 inventory slots from first slot."""
        first_x, first_y = self.positions['inv_first_slot']
        
        slots = []
        for row in range(7):
            for col in range(4):
                x = first_x + (col * 42)
                y = first_y + (row * 36)
                slots.append((x, y))
        
        self.positions['inventory_slots'] = slots
        print(f"✅ Calculated {len(slots)} inventory slots")
    
    def _save_setup(self):
        """Save setup to file."""
        # Convert to JSON-serializable format
        data = dict(self.positions)
        
        with open('setup.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_setup(self):
        """Load setup from file."""
        if not Path('setup.json').exists():
            return False
        
        try:
            with open('setup.json', 'r') as f:
                self.positions = json.load(f)
            
            print("✅ Loaded setup from setup.json")
            return True
        except Exception as e:
            print(f"⚠️  Failed to load setup: {e}")
            return False


class BezierMovement:
    """Smooth mouse movements."""
    
    @staticmethod
    def move_click(target_x, target_y):
        """Move and click with Bezier curve."""
        start = pyautogui.position()
        
        # Add randomness
        target_x += random.randint(-3, 3)
        target_y += random.randint(-3, 3)
        
        # Generate curve
        distance = math.sqrt((target_x - start[0])**2 + (target_y - start[1])**2)
        num_points = max(10, int(distance / 30))
        
        # Control points
        ctrl1_x = start[0] + (target_x - start[0]) * 0.25 + random.randint(-20, 20)
        ctrl1_y = start[1] + (target_y - start[1]) * 0.25 + random.randint(-20, 20)
        ctrl2_x = start[0] + (target_x - start[0]) * 0.75 + random.randint(-20, 20)
        ctrl2_y = start[1] + (target_y - start[1]) * 0.75 + random.randint(-20, 20)
        
        # Move along curve
        for i in range(num_points + 1):
            t = i / num_points
            x = ((1-t)**3 * start[0] + 3*(1-t)**2*t * ctrl1_x + 
                 3*(1-t)*t**2 * ctrl2_x + t**3 * target_x)
            y = ((1-t)**3 * start[1] + 3*(1-t)**2*t * ctrl1_y + 
                 3*(1-t)*t**2 * ctrl2_y + t**3 * target_y)
            
            pyautogui.moveTo(int(x), int(y))
            time.sleep(random.uniform(0.001, 0.003))
        
        # Click
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.click()


class HerbloreBot:
    """Main bot using F-key setup."""
    
    def __init__(self, setup, potion_name):
        self.setup = setup
        self.potion_name = potion_name
        self.potions_made = 0
        self.running = True
        
        # Load potion data
        with open('data/potions.json', 'r') as f:
            data = json.load(f)
            potions = {p['name']: p for p in data['potions']}
            self.potion = potions[potion_name]
        
        print(f"\n[BOT] Potion: {self.potion['name']}")
        print(f"[BOT] Herb: {self.potion['herb']}")
        print(f"[BOT] XP: {self.potion['xp']}")
    
    def start(self):
        """Start the bot."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print("="*60)
        print("\n⚠️  Move mouse to TOP-LEFT corner to stop")
        print("⚠️  Or press Ctrl+C\n")
        
        input("Press Enter to start...")
        
        start_time = datetime.now()
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                # Bank
                self._bank()
                
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
    
    def _bank(self):
        """Banking."""
        print("[BANKING]")
        
        # Click bank
        print("  Opening bank...")
        bank_x, bank_y = self.setup.positions['bank']
        BezierMovement.move_click(bank_x, bank_y)
        time.sleep(random.uniform(1.5, 2.0))
        
        # Deposit all
        print("  Depositing inventory...")
        dep_x, dep_y = self.setup.positions['deposit_button']
        BezierMovement.move_click(dep_x, dep_y)
        time.sleep(random.uniform(0.6, 0.9))
        
        # Withdraw herbs
        print(f"  Withdrawing {self.potion['herb']}...")
        herb_x, herb_y = self.setup.positions['herb_slot']
        BezierMovement.move_click(herb_x, herb_y)
        time.sleep(0.3)
        
        # Right-click and withdraw-all
        pyautogui.click(button='right')
        time.sleep(0.3)
        pyautogui.moveRel(0, 60)  # Move to withdraw-all option
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 0.9))
        
        # Withdraw vials
        print("  Withdrawing vials...")
        vial_x, vial_y = self.setup.positions['vial_slot']
        BezierMovement.move_click(vial_x, vial_y)
        time.sleep(0.3)
        pyautogui.click(button='right')
        time.sleep(0.3)
        pyautogui.moveRel(0, 60)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 0.9))
        
        # Close bank
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print("  ✅ Banking complete")
    
    def _make_potions(self):
        """Make potions."""
        print("\n[MAKING POTIONS]")
        
        slots = self.setup.positions['inventory_slots']
        
        # Click first herb (slot 1)
        print("  Clicking herb...")
        herb_x, herb_y = slots[0]
        BezierMovement.move_click(herb_x, herb_y)
        time.sleep(random.uniform(0.3, 0.5))
        
        # Click first vial (slot 15, assuming 14 herbs)
        print("  Clicking vial...")
        vial_x, vial_y = slots[14]
        BezierMovement.move_click(vial_x, vial_y)
        time.sleep(random.uniform(0.8, 1.2))
        
        # Press space
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Wait
        wait_time = 28
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
    
    # Setup
    setup = FKeySetup()
    
    # Try to load existing setup
    if setup.load_setup():
        reuse = input("\nReuse saved setup? (y/n): ").strip().lower()
        if reuse != 'y':
            setup.run_setup()
    else:
        setup.run_setup()
    
    # Create and start bot
    bot = HerbloreBot(setup, potion['name'])
    bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
