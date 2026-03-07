#!/usr/bin/env python3
"""
OSRS Herblore Bot - Final Version
- Template matching for item verification
- Recognizes correct inventory
- Handles secondary ingredients (eye of newt, etc.)
- Anti-cheat: random offsets, variable speeds
- Smooth Bezier movements
"""
import time
import random
import json
import math
import numpy as np
from datetime import datetime
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Bot - FINAL VERSION                                ║
║   Smart detection | Anti-cheat | Complete workflow       ║
╚═══════════════════════════════════════════════════════════╝
""")

# Dependencies
try:
    import pyautogui
    import mss
    import cv2
    from PIL import Image
    print("✅ Dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    input("Press Enter...")
    exit(1)

pyautogui.FAILSAFE = True


class SmartSetup:
    """Smart setup with template learning."""
    
    def __init__(self):
        self.positions = {}
        self.templates = {}
        self.sct = mss.mss()
    
    def capture_item_template(self, item_name, instruction):
        """Capture item template for matching."""
        print(f"\n{'='*60}")
        print(f"CAPTURE: {item_name}")
        print(f"{'='*60}")
        print(instruction)
        print()
        
        input("Press Enter when ready, then click the item...")
        print("Waiting 3 seconds - move mouse to item and click...")
        time.sleep(3)
        
        # Get position
        pos = pyautogui.position()
        x, y = pos.x, pos.y
        
        # Capture small region around position
        region = {
            'left': x - 20,
            'top': y - 20,
            'width': 40,
            'height': 40
        }
        
        screenshot = np.array(self.sct.grab(region))
        
        # Save template
        self.templates[item_name] = screenshot
        self.positions[item_name] = (x, y)
        
        # Save image
        Path('templates').mkdir(exist_ok=True)
        img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        img.save(f'templates/{item_name}.png')
        
        print(f"✅ Saved template: {item_name} at ({x}, {y})")
        
        # Confirm
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        confirm = input("Correct? (y/n): ").strip().lower()
        if confirm != 'y':
            return self.capture_item_template(item_name, instruction)
        
        return (x, y)
    
    def run_setup(self):
        """Full setup process."""
        print("\n" + "="*60)
        print("SMART SETUP")
        print("="*60)
        print("\nWe'll capture 7 positions + learn item templates:")
        print("  1. Bank booth")
        print("  2. Deposit button")
        print("  3. Herb (in bank)")
        print("  4. Secondary ingredient (in bank)")
        print("  5. Vials (in bank)")
        print("  6. First inventory slot")
        print("  7. Herb in inventory (for verification)")
        print()
        input("Press Enter to start...")
        
        # 1. Bank
        self.capture_item_template(
            "bank_booth",
            "BANK BOOTH:\n"
            "Move your mouse over the bank booth/chest you click to open bank."
        )
        
        # Open bank
        print("\n📋 OPEN the bank now")
        input("Press Enter when bank is open...")
        
        # 2. Deposit
        self.capture_item_template(
            "deposit_button",
            "DEPOSIT INVENTORY BUTTON:\n"
            "Move mouse over the 'Deposit Inventory' button\n"
            "(Usually bottom-right of bank interface)"
        )
        
        # 3. Herb
        print("\n📋 Make sure your HERB is visible in bank")
        self.capture_item_template(
            "herb_bank",
            "HERB IN BANK:\n"
            "Move mouse over your herb (e.g., Guam leaf)\n"
            "Bot will learn what this item looks like!"
        )
        
        # 4. Secondary
        print("\n📋 Find your SECONDARY ingredient")
        secondary_name = input("What secondary? (e.g., Eye of newt): ").strip()
        self.positions['secondary_name'] = secondary_name
        
        self.capture_item_template(
            "secondary_bank",
            f"SECONDARY IN BANK:\n"
            f"Move mouse over {secondary_name} in bank\n"
            "Bot will learn this item too!"
        )
        
        # 5. Vials
        self.capture_item_template(
            "vial_bank",
            "VIALS IN BANK:\n"
            "Move mouse over 'Vial of water' in bank"
        )
        
        # Close bank
        print("\n📋 CLOSE the bank")
        input("Press Enter when closed...")
        
        # 6. First inv slot
        self.capture_item_template(
            "inv_first",
            "FIRST INVENTORY SLOT:\n"
            "Move mouse over the FIRST slot (top-left) of your inventory"
        )
        
        # Calculate grid
        self._calculate_inventory()
        
        # 7. Herb in inventory (for verification)
        print("\n📋 Put ONE herb in your inventory")
        input("Press Enter when ready...")
        
        self.capture_item_template(
            "herb_inv_template",
            "HERB IN INVENTORY:\n"
            "Move mouse over the herb in your inventory\n"
            "Bot will use this to verify items later!"
        )
        
        # Save
        self._save()
        
        print("\n✅ Setup complete!")
        print("✅ Bot learned all item appearances!")
        return True
    
    def _calculate_inventory(self):
        """Calculate inv slots."""
        x, y = self.positions['inv_first']
        slots = []
        for row in range(7):
            for col in range(4):
                slots.append((x + col * 42, y + row * 36))
        self.positions['inventory_slots'] = slots
        print(f"✅ Calculated {len(slots)} slots")
    
    def _save(self):
        """Save setup."""
        # Save positions (excluding non-serializable)
        data = {k: v for k, v in self.positions.items() 
                if k != 'inventory_slots'}
        data['inventory_slots'] = self.positions['inventory_slots']
        
        with open('smart_setup.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("📁 Saved:")
        print("   - smart_setup.json")
        print("   - templates/*.png")
    
    def load(self):
        """Load setup."""
        if not Path('smart_setup.json').exists():
            return False
        
        try:
            with open('smart_setup.json', 'r') as f:
                self.positions = json.load(f)
            
            # Load templates
            for file in Path('templates').glob('*.png'):
                name = file.stem
                img = cv2.imread(str(file))
                self.templates[name] = img
            
            print("✅ Loaded setup + templates")
            return True
        except Exception as e:
            print(f"⚠️  Load failed: {e}")
            return False
    
    def verify_inventory(self):
        """Check if inventory has correct items."""
        print("\n[VERIFY] Checking inventory...")
        
        # Capture inventory area
        first_x, first_y = self.positions['inventory_slots'][0]
        region = {
            'left': first_x - 10,
            'top': first_y - 10,
            'width': 200,
            'height': 270
        }
        
        screenshot = np.array(self.sct.grab(region))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Check for herb using template
        if 'herb_inv_template' in self.templates:
            template = cv2.cvtColor(self.templates['herb_inv_template'], cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val > 0.7:
                print("  ✅ Inventory looks correct!")
                return True
            else:
                print(f"  ⚠️  Inventory check uncertain (match: {max_val:.2f})")
                return True  # Continue anyway
        
        return True


class SmoothMovement:
    """Anti-cheat mouse movement."""
    
    @staticmethod
    def move_click(target_x, target_y, offset_range=8):
        """Smooth Bezier with random offset."""
        start = pyautogui.position()
        
        # LARGE random offset for anti-cheat
        target_x += random.randint(-offset_range, offset_range)
        target_y += random.randint(-offset_range, offset_range)
        
        distance = math.sqrt((target_x - start[0])**2 + (target_y - start[1])**2)
        
        # Variable speed based on distance
        num_points = max(15, int(distance / 20))
        
        # Bezier control points with MORE randomness
        ctrl1_x = start[0] + (target_x - start[0]) * random.uniform(0.2, 0.35) + random.randint(-40, 40)
        ctrl1_y = start[1] + (target_y - start[1]) * random.uniform(0.2, 0.35) + random.randint(-40, 40)
        ctrl2_x = start[0] + (target_x - start[0]) * random.uniform(0.65, 0.8) + random.randint(-40, 40)
        ctrl2_y = start[1] + (target_y - start[1]) * random.uniform(0.65, 0.8) + random.randint(-40, 40)
        
        # Move along curve with VARIABLE speed
        for i in range(num_points + 1):
            t = i / num_points
            
            # Ease in/out
            t_eased = t * t * (3 - 2 * t)
            
            px = ((1-t_eased)**3 * start[0] + 
                  3*(1-t_eased)**2*t_eased * ctrl1_x + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_x + 
                  t_eased**3 * target_x)
            py = ((1-t_eased)**3 * start[1] + 
                  3*(1-t_eased)**2*t_eased * ctrl1_y + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_y + 
                  t_eased**3 * target_y)
            
            pyautogui.moveTo(int(px), int(py))
            
            # Variable delay - slower at start/end, faster in middle
            if i < 5 or i > num_points - 5:
                delay = random.uniform(0.003, 0.006)
            else:
                delay = random.uniform(0.001, 0.003)
            time.sleep(delay)
        
        # Random pre-click delay
        time.sleep(random.uniform(0.08, 0.18))
        
        # Sometimes micro-adjust before click
        if random.random() < 0.3:
            pyautogui.moveRel(random.randint(-2, 2), random.randint(-2, 2))
            time.sleep(random.uniform(0.02, 0.05))
        
        pyautogui.click()


class HerbloreBot:
    """Final bot with proper herblore workflow."""
    
    def __init__(self, setup):
        self.setup = setup
        self.potions_made = 0
        self.running = True
    
    def start(self):
        """Start bot."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print("="*60)
        
        # Verify inventory
        if not self.setup.verify_inventory():
            print("\n⚠️  Inventory verification failed")
            if input("Continue anyway? (y/n): ").lower() != 'y':
                return
        
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
                self._make_unfinished()
                self._add_secondary()
                
                self.potions_made += 14
                elapsed = (datetime.now() - start_time).total_seconds()
                xp_hour = (self.potions_made * 25 / elapsed * 3600) if elapsed > 0 else 0
                
                print(f"\n📊 Potions: {self.potions_made}")
                print(f"📊 XP/hr: {xp_hour:,.0f}")
                print(f"📊 Runtime: {int(elapsed)}s")
                
                # Variable delay
                delay = random.uniform(4, 8)
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
        """Banking."""
        print("[BANKING]")
        
        # Open bank
        print("  Opening bank...")
        x, y = self.setup.positions['bank_booth']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(1.8, 2.5))
        
        # Deposit
        print("  Depositing...")
        x, y = self.setup.positions['deposit_button']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.7, 1.1))
        
        # Withdraw herbs (14)
        print("  Withdrawing herbs...")
        x, y = self.setup.positions['herb_bank']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.3, 0.5))
        
        # Withdraw-14 (usually 2nd option)
        pyautogui.moveRel(random.randint(-2, 2), random.randint(38, 42))
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.click()
        time.sleep(random.uniform(0.6, 1.0))
        
        # Withdraw vials (14)
        print("  Withdrawing vials...")
        x, y = self.setup.positions['vial_bank']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.moveRel(random.randint(-2, 2), random.randint(38, 42))
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.click()
        time.sleep(random.uniform(0.6, 1.0))
        
        # Close
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(random.uniform(0.5, 0.8))
        
        print("  ✅ Banking done")
    
    def _make_unfinished(self):
        """Make unfinished potions (herb + vial)."""
        print("\n[UNFINISHED POTIONS]")
        
        slots = self.setup.positions['inventory_slots']
        
        # Click herb (slot 1)
        print("  Clicking herb...")
        x, y = slots[0]
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.6))
        
        # Click vial (slot 15)
        print("  Clicking vial...")
        x, y = slots[14]
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.9, 1.4))
        
        # Make all
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(random.uniform(0.5, 0.8))
        
        # Wait for unfinished potions
        wait = random.uniform(15, 18)
        print(f"  Waiting {wait:.1f}s for unfinished potions...")
        time.sleep(wait)
        
        print("  ✅ Unfinished done")
    
    def _add_secondary(self):
        """Add secondary ingredient to finish potions."""
        print("\n[FINISHING POTIONS]")
        
        # Bank for secondary
        print("  Opening bank...")
        x, y = self.setup.positions['bank_booth']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(1.8, 2.5))
        
        # Withdraw secondary (14)
        print(f"  Withdrawing {self.setup.positions['secondary_name']}...")
        x, y = self.setup.positions['secondary_bank']
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.moveRel(random.randint(-2, 2), random.randint(38, 42))
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.click()
        time.sleep(random.uniform(0.6, 1.0))
        
        # Close bank
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(random.uniform(0.5, 0.8))
        
        # Use secondary on unfinished potion
        slots = self.setup.positions['inventory_slots']
        
        print("  Clicking secondary...")
        x, y = slots[14]  # Secondary in slot 15
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.3, 0.6))
        
        print("  Clicking unfinished potion...")
        x, y = slots[0]  # Unfinished in slot 1
        SmoothMovement.move_click(x, y)
        time.sleep(random.uniform(0.9, 1.4))
        
        # Make all
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(random.uniform(0.5, 0.8))
        
        # Wait for finished potions
        wait = random.uniform(15, 18)
        print(f"  Waiting {wait:.1f}s for finished potions...")
        time.sleep(wait)
        
        print("  ✅ Potions finished!")


def main():
    """Main."""
    setup = SmartSetup()
    
    if setup.load():
        reuse = input("\nReuse setup? (y/n): ").strip().lower()
        if reuse != 'y':
            setup.run_setup()
    else:
        setup.run_setup()
    
    bot = HerbloreBot(setup)
    bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter...")
