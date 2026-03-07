#!/usr/bin/env python3
"""
OSRS Herblore Bot - F8 Screenshot Detection
Press F8 to capture and auto-detect positions
"""
import time
import random
import json
import math
import numpy as np
from datetime import datetime
from pathlib import Path
from pynput import keyboard
from PIL import Image

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Bot - F8 Screenshot Detection                     ║
║   Press F8 → Bot captures & detects everything!          ║
╚═══════════════════════════════════════════════════════════╝
""")

# Dependencies
try:
    import pyautogui
    import mss
    import cv2
    print("✅ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Install: pip install pyautogui mss opencv-python pillow numpy pynput")
    input("Press Enter to exit...")
    exit(1)

# Config
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


class ScreenshotSetup:
    """F8 screenshot-based setup."""
    
    def __init__(self):
        self.sct = mss.mss()
        self.templates = {}
        self.positions = {}
        self.screenshots = []
        self.f8_pressed = False
        self.listener = None
        self.setup_complete = False
    
    def on_press(self, key):
        """Handle F8 press."""
        try:
            if key == keyboard.Key.f8:
                self.f8_pressed = True
        except AttributeError:
            pass
    
    def wait_for_f8(self, step_name, instruction):
        """Wait for F8 screenshot."""
        print(f"\n{'='*60}")
        print(f"STEP: {step_name}")
        print(f"{'='*60}")
        print(instruction)
        print("\n👉 Set up the screen as instructed")
        print("👉 Press F8 to capture")
        print()
        
        self.f8_pressed = False
        
        # Start listener
        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
        
        # Wait for F8
        while not self.f8_pressed:
            time.sleep(0.1)
        
        # Capture screenshot
        screenshot = np.array(self.sct.grab(self.sct.monitors[0]))
        self.screenshots.append({
            'name': step_name,
            'image': screenshot,
            'timestamp': datetime.now()
        })
        
        print(f"✅ Screenshot captured: {step_name}")
        
        # Save screenshot
        Path('screenshots').mkdir(exist_ok=True)
        img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        img.save(f'screenshots/{step_name}.png')
        print(f"   Saved to screenshots/{step_name}.png")
        
        time.sleep(0.5)
        return screenshot
    
    def run_setup(self):
        """Run F8 guided setup."""
        print("\n" + "="*60)
        print("F8 GUIDED SETUP")
        print("="*60)
        print("\nWe'll capture 3 screenshots:")
        print("  1. Inventory with herbs & vials")
        print("  2. Bank open with items visible")
        print("  3. Game ready to start")
        print()
        input("Press Enter to start...")
        
        # Step 1: Inventory with items
        ss1 = self.wait_for_f8(
            "inventory_with_items",
            "STEP 1: INVENTORY WITH ITEMS\n"
            "1. Put some herbs in your inventory (any amount)\n"
            "2. Put some vials of water in your inventory\n"
            "3. Make sure inventory tab is visible\n"
            "4. Press F8"
        )
        
        # Detect items in inventory
        print("\n[DETECTION] Finding items in inventory...")
        self._detect_inventory_items(ss1)
        
        # Step 2: Bank open
        ss2 = self.wait_for_f8(
            "bank_open",
            "STEP 2: BANK INTERFACE\n"
            "1. OPEN your bank (click the booth/chest)\n"
            "2. Make sure the SAME herbs are visible in bank\n"
            "3. Make sure vials are visible in bank\n"
            "4. Keep bank interface open\n"
            "5. Press F8"
        )
        
        # Detect bank items and positions
        print("\n[DETECTION] Finding items in bank...")
        self._detect_bank_items(ss2)
        
        # Step 3: Ready state
        print("\n📋 Close the bank (press ESC)")
        input("Press Enter once bank is closed...")
        
        ss3 = self.wait_for_f8(
            "ready_state",
            "STEP 3: READY TO START\n"
            "1. Stand at the bank\n"
            "2. Inventory should be empty or ready\n"
            "3. Press F8"
        )
        
        # Detect bank booth in game view
        print("\n[DETECTION] Finding bank booth...")
        self._detect_bank_booth(ss3)
        
        # Save setup
        self._save_setup()
        
        print("\n✅ Setup complete!")
        print("✅ All templates and positions saved!")
        
        # Stop listener
        if self.listener:
            self.listener.stop()
        
        self.setup_complete = True
        return True
    
    def _detect_inventory_items(self, screenshot):
        """Detect herb and vial positions in inventory."""
        print("  Scanning inventory...")
        
        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Known inventory grid positions (RuneLite fixed mode)
        # We'll scan a region where inventory usually is
        
        # For now, use color detection to find brown (herbs) and blue (vials)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Green/brown for herbs
        lower_herb = np.array([20, 30, 30])
        upper_herb = np.array([80, 255, 255])
        herb_mask = cv2.inRange(hsv, lower_herb, upper_herb)
        
        # Blue for vials
        lower_vial = np.array([90, 50, 50])
        upper_vial = np.array([130, 255, 255])
        vial_mask = cv2.inRange(hsv, lower_vial, upper_vial)
        
        # Find contours
        herb_contours, _ = cv2.findContours(herb_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        vial_contours, _ = cv2.findContours(vial_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get first herb position
        if herb_contours:
            largest_herb = max(herb_contours, key=cv2.contourArea)
            M = cv2.moments(largest_herb)
            if M['m00'] > 0:
                herb_x = int(M['m10'] / M['m00'])
                herb_y = int(M['m01'] / M['m00'])
                self.positions['herb_inv'] = (herb_x, herb_y)
                print(f"  ✅ Found herb at ({herb_x}, {herb_y})")
                
                # Save template
                x, y, w, h = cv2.boundingRect(largest_herb)
                self.templates['herb'] = screenshot[y:y+h, x:x+w]
        
        # Get first vial position
        if vial_contours:
            largest_vial = max(vial_contours, key=cv2.contourArea)
            M = cv2.moments(largest_vial)
            if M['m00'] > 0:
                vial_x = int(M['m10'] / M['m00'])
                vial_y = int(M['m01'] / M['m00'])
                self.positions['vial_inv'] = (vial_x, vial_y)
                print(f"  ✅ Found vial at ({vial_x}, {vial_y})")
                
                # Save template
                x, y, w, h = cv2.boundingRect(largest_vial)
                self.templates['vial'] = screenshot[y:y+h, x:x+w]
        
        # Calculate inventory grid from first item
        if 'herb_inv' in self.positions:
            self._calculate_inventory_grid()
    
    def _calculate_inventory_grid(self):
        """Calculate all 28 inventory slots."""
        # Estimate first slot position from detected herb
        herb_x, herb_y = self.positions['herb_inv']
        
        # Inventory slots are ~42x36 pixels apart
        # Estimate top-left of first slot
        first_x = herb_x - (herb_x % 42)
        first_y = herb_y - (herb_y % 36)
        
        # Calculate all slots
        slots = []
        for row in range(7):
            for col in range(4):
                x = first_x + (col * 42)
                y = first_y + (row * 36)
                slots.append((x, y))
        
        self.positions['inventory_slots'] = slots
        print(f"  ✅ Calculated {len(slots)} inventory slots")
    
    def _detect_bank_items(self, screenshot):
        """Detect herb and vial in bank using templates."""
        print("  Searching for items in bank...")
        
        if 'herb' not in self.templates:
            print("  ⚠️  No herb template - using color detection")
            return
        
        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        herb_template = cv2.cvtColor(self.templates['herb'], cv2.COLOR_BGR2GRAY)
        
        # Template match for herb
        result = cv2.matchTemplate(gray, herb_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.6:  # Good match
            h, w = herb_template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            self.positions['herb_bank'] = (center_x, center_y)
            print(f"  ✅ Found herb in bank at ({center_x}, {center_y})")
        
        # Template match for vial
        if 'vial' in self.templates:
            vial_template = cv2.cvtColor(self.templates['vial'], cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray, vial_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.6:
                h, w = vial_template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                self.positions['vial_bank'] = (center_x, center_y)
                print(f"  ✅ Found vial in bank at ({center_x}, {center_y})")
        
        # Find deposit button (usually bottom-right of bank)
        # Look for brown button color
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower = np.array([10, 100, 100])
        upper = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find bottommost contour (likely deposit button)
            bottom_contour = max(contours, key=lambda c: cv2.boundingRect(c)[1])
            x, y, w, h = cv2.boundingRect(bottom_contour)
            self.positions['deposit_button'] = (x + w//2, y + h//2)
            print(f"  ✅ Found deposit button at ({x + w//2}, {y + h//2})")
    
    def _detect_bank_booth(self, screenshot):
        """Detect bank booth in game view."""
        print("  Looking for bank booth...")
        
        # Bank booths are brown/tan colored
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower = np.array([5, 50, 50])
        upper = np.array([25, 255, 200])
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Largest brown area in center of screen
            valid_contours = [c for c in contours if cv2.contourArea(c) > 500]
            if valid_contours:
                largest = max(valid_contours, key=cv2.contourArea)
                M = cv2.moments(largest)
                if M['m00'] > 0:
                    bank_x = int(M['m10'] / M['m00'])
                    bank_y = int(M['m01'] / M['m00'])
                    self.positions['bank_booth'] = (bank_x, bank_y)
                    print(f"  ✅ Found bank booth at ({bank_x}, {bank_y})")
                    return
        
        print("  ⚠️  Could not auto-detect bank - will use center of viewport")
        # Fallback: center of game viewport
        self.positions['bank_booth'] = (screenshot.shape[1] // 3, screenshot.shape[0] // 3)
    
    def _save_setup(self):
        """Save setup to file."""
        # Save templates as images
        Path('templates').mkdir(exist_ok=True)
        for name, template in self.templates.items():
            cv2.imwrite(f'templates/{name}.png', template)
        
        # Save positions
        data = {k: v for k, v in self.positions.items() if k != 'inventory_slots'}
        if 'inventory_slots' in self.positions:
            data['inventory_slots'] = self.positions['inventory_slots']
        
        with open('bot_setup.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("\n📁 Saved:")
        print("   - bot_setup.json (positions)")
        print("   - templates/*.png (item images)")
        print("   - screenshots/*.png (reference)")
    
    def load_setup(self):
        """Load saved setup."""
        if not Path('bot_setup.json').exists():
            return False
        
        try:
            with open('bot_setup.json', 'r') as f:
                self.positions = json.load(f)
            
            # Load templates
            for template_file in Path('templates').glob('*.png'):
                name = template_file.stem
                self.templates[name] = cv2.imread(str(template_file))
            
            print("✅ Loaded saved setup")
            return True
        except Exception as e:
            print(f"⚠️  Failed to load: {e}")
            return False


class BezierMovement:
    """Smooth Bezier movements."""
    
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


class HerbloreBot:
    """Bot using screenshot setup."""
    
    def __init__(self, setup):
        self.setup = setup
        self.potions_made = 0
        self.running = True
    
    def start(self):
        """Start bot."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print("="*60)
        print("\n⚠️  Move mouse to corner to stop")
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
                
                self._bank()
                self._make_potions()
                
                self.potions_made += 14
                elapsed = (datetime.now() - start_time).total_seconds()
                
                print(f"\n📊 Stats:")
                print(f"  Potions: {self.potions_made}")
                print(f"  Runtime: {int(elapsed)}s")
                
                delay = random.uniform(3, 6)
                print(f"\n⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\n[BOT] Stopped")
        except pyautogui.FailSafeException:
            print("\n\n[BOT] FAILSAFE")
        finally:
            print("\n" + "="*60)
            print("BOT STOPPED")
            print("="*60)
    
    def _bank(self):
        """Bank."""
        print("[BANKING]")
        
        # Click bank
        if 'bank_booth' in self.setup.positions:
            print("  Opening bank...")
            x, y = self.setup.positions['bank_booth']
            BezierMovement.move_click(x, y)
            time.sleep(random.uniform(1.5, 2.0))
        
        # Deposit
        if 'deposit_button' in self.setup.positions:
            print("  Depositing...")
            x, y = self.setup.positions['deposit_button']
            BezierMovement.move_click(x, y)
            time.sleep(random.uniform(0.6, 0.9))
        
        # Withdraw herbs
        if 'herb_bank' in self.setup.positions:
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
        
        # Withdraw vials
        if 'vial_bank' in self.setup.positions:
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
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print("  ✅ Banking complete")
    
    def _make_potions(self):
        """Make potions."""
        print("\n[MAKING POTIONS]")
        
        if 'inventory_slots' not in self.setup.positions:
            print("  ⚠️  No inventory slots - using detected positions")
            if 'herb_inv' in self.setup.positions:
                herb_x, herb_y = self.setup.positions['herb_inv']
            if 'vial_inv' in self.setup.positions:
                vial_x, vial_y = self.setup.positions['vial_inv']
        else:
            slots = self.setup.positions['inventory_slots']
            herb_x, herb_y = slots[0]
            vial_x, vial_y = slots[14]
        
        # Click herb
        print("  Clicking herb...")
        BezierMovement.move_click(herb_x, herb_y)
        time.sleep(random.uniform(0.3, 0.5))
        
        # Click vial
        print("  Clicking vial...")
        BezierMovement.move_click(vial_x, vial_y)
        time.sleep(random.uniform(0.8, 1.2))
        
        # Space
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Wait
        print("  Waiting 28s...")
        time.sleep(28)
        
        print("  ✅ Potions made")


def main():
    """Main."""
    setup = ScreenshotSetup()
    
    # Load or create setup
    if setup.load_setup():
        reuse = input("\nReuse saved setup? (y/n): ").strip().lower()
        if reuse != 'y':
            setup.run_setup()
    else:
        setup.run_setup()
    
    # Start bot
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
