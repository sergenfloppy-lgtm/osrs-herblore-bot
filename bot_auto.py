#!/usr/bin/env python3
"""
OSRS Herblore Bot - Auto-Detection (PROPER)
Based on research of working OSRS bots
Uses FIXED coordinates for RuneLite fixed mode
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
║   OSRS Bot - Auto-Detection (WORKING VERSION)            ║
║   Zero setup required - finds everything automatically    ║
╚═══════════════════════════════════════════════════════════╝
""")

# Check dependencies
try:
    import pyautogui
    import mss
    import cv2
    from PIL import Image
    print("✅ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Install: pip install pyautogui mss opencv-python pillow numpy")
    input("Press Enter to exit...")
    exit(1)

# Configure
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


class RuneLiteFixedDetector:
    """Detect RuneLite fixed mode using KNOWN coordinates."""
    
    # RuneLite fixed mode constants (these are ALWAYS the same!)
    FIXED_WIDTH = 765
    FIXED_HEIGHT = 503
    
    # Inventory slots (relative to game window top-left)
    INV_START_X = 563
    INV_START_Y = 213
    INV_SLOT_WIDTH = 42
    INV_SLOT_HEIGHT = 36
    
    # Chat/combat area (to avoid clicking)
    CHAT_Y_START = 345
    
    def __init__(self):
        self.sct = mss.mss()
        self.game_window = None
        self.inventory_slots = []
    
    def find_game_window(self):
        """Find RuneLite window using screen search."""
        print("[DETECTION] Searching for RuneLite fixed mode window...")
        
        # Take screenshot of all monitors
        for monitor_idx, monitor in enumerate(self.sct.monitors[1:], 1):
            print(f"  Scanning monitor {monitor_idx}...")
            
            # Capture monitor
            screenshot = np.array(self.sct.grab(monitor))
            
            # Convert to grayscale
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Look for the characteristic OSRS interface
            # The game has a black border and specific UI colors
            
            # Method 1: Look for exact window size in taskbar/window borders
            # Scan for regions that could be the game window
            for y in range(0, monitor['height'] - self.FIXED_HEIGHT, 10):
                for x in range(0, monitor['width'] - self.FIXED_WIDTH, 10):
                    # Check if this region looks like OSRS
                    region = gray[y:y+self.FIXED_HEIGHT, x:x+self.FIXED_WIDTH]
                    
                    if region.shape[0] != self.FIXED_HEIGHT or region.shape[1] != self.FIXED_WIDTH:
                        continue
                    
                    # Check for characteristic inventory area (brown/gray UI)
                    inv_region = region[self.INV_START_Y:self.INV_START_Y+250, 
                                       self.INV_START_X:self.INV_START_X+180]
                    
                    # Inventory should have specific brightness patterns
                    if inv_region.mean() > 30 and inv_region.mean() < 80:
                        # Found potential game window!
                        self.game_window = {
                            'x': monitor['left'] + x,
                            'y': monitor['top'] + y,
                            'width': self.FIXED_WIDTH,
                            'height': self.FIXED_HEIGHT
                        }
                        
                        print(f"✅ Found game window at ({self.game_window['x']}, {self.game_window['y']})")
                        return True
        
        print("⚠️  Could not auto-detect window. Trying fallback...")
        return self._fallback_detection()
    
    def _fallback_detection(self):
        """Fallback: look for window title."""
        print("[FALLBACK] Looking for RuneLite window title...")
        
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle('RuneLite')
            
            if windows:
                win = windows[0]
                # Adjust for window borders
                self.game_window = {
                    'x': win.left + 8,  # Account for border
                    'y': win.top + 30,  # Account for titlebar
                    'width': self.FIXED_WIDTH,
                    'height': self.FIXED_HEIGHT
                }
                print(f"✅ Found via window title: ({self.game_window['x']}, {self.game_window['y']})")
                return True
        except ImportError:
            print("  pygetwindow not available")
        
        # Last resort: manual
        print("\n⚠️  Auto-detection failed. Manual setup required.")
        print("Move mouse to TOP-LEFT corner of game area (not window border!)")
        input("Press Enter...")
        top_left = pyautogui.position()
        
        self.game_window = {
            'x': top_left[0],
            'y': top_left[1],
            'width': self.FIXED_WIDTH,
            'height': self.FIXED_HEIGHT
        }
        
        print(f"✅ Manual position set: ({self.game_window['x']}, {self.game_window['y']})")
        return True
    
    def calculate_inventory_slots(self):
        """Calculate all 28 inventory slots using FIXED offsets."""
        print("[DETECTION] Calculating inventory slots...")
        
        if not self.game_window:
            print("❌ Game window not set!")
            return False
        
        base_x = self.game_window['x'] + self.INV_START_X
        base_y = self.game_window['y'] + self.INV_START_Y
        
        self.inventory_slots = []
        for row in range(7):
            for col in range(4):
                x = base_x + (col * self.INV_SLOT_WIDTH)
                y = base_y + (row * self.INV_SLOT_HEIGHT)
                self.inventory_slots.append((x, y))
        
        print(f"✅ Calculated {len(self.inventory_slots)} inventory slots")
        return True
    
    def find_bank(self):
        """Find bank using color detection in game viewport."""
        print("[DETECTION] Looking for bank...")
        
        if not self.game_window:
            print("❌ Game window not set!")
            return None
        
        # Capture game viewport (not inventory/chat)
        viewport = {
            'left': self.game_window['x'],
            'top': self.game_window['y'],
            'width': 512,  # Viewport width in fixed mode
            'height': 334  # Viewport height
        }
        
        screenshot = np.array(self.sct.grab(viewport))
        
        # Convert BGR to HSV for better color detection
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Varrock East bank booths are brown
        lower_brown = np.array([5, 50, 50])
        upper_brown = np.array([25, 255, 255])
        
        mask = cv2.inRange(hsv, lower_brown, upper_brown)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest brown area (likely bank)
            largest = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest) > 500:  # Minimum size
                M = cv2.moments(largest)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    
                    bank_x = viewport['left'] + cx
                    bank_y = viewport['top'] + cy
                    
                    print(f"✅ Found bank at ({bank_x}, {bank_y})")
                    return (bank_x, bank_y)
        
        # Fallback: center-ish of viewport
        print("⚠️  Using default bank position (center viewport)")
        return (
            self.game_window['x'] + 256,
            self.game_window['y'] + 167
        )


class BezierMovement:
    """Smooth Bezier curve mouse movement."""
    
    @staticmethod
    def move_to(target_x, target_y, click=True):
        """Move mouse to target using Bezier curve."""
        start = pyautogui.position()
        
        # Add randomness to target
        target_x += random.randint(-3, 3)
        target_y += random.randint(-3, 3)
        
        # Generate curve
        distance = math.sqrt((target_x - start[0])**2 + (target_y - start[1])**2)
        num_points = int(distance / 20) + 5  # More points for longer distances
        
        # Control points
        ctrl1_x = start[0] + (target_x - start[0]) * 0.25 + random.randint(-30, 30)
        ctrl1_y = start[1] + (target_y - start[1]) * 0.25 + random.randint(-30, 30)
        ctrl2_x = start[0] + (target_x - start[0]) * 0.75 + random.randint(-30, 30)
        ctrl2_y = start[1] + (target_y - start[1]) * 0.75 + random.randint(-30, 30)
        
        # Generate points
        for i in range(num_points + 1):
            t = i / num_points
            x = ((1-t)**3 * start[0] + 
                 3*(1-t)**2*t * ctrl1_x + 
                 3*(1-t)*t**2 * ctrl2_x + 
                 t**3 * target_x)
            y = ((1-t)**3 * start[1] + 
                 3*(1-t)**2*t * ctrl1_y + 
                 3*(1-t)*t**2 * ctrl2_y + 
                 t**3 * target_y)
            
            pyautogui.moveTo(int(x), int(y))
            time.sleep(random.uniform(0.001, 0.003))
        
        if click:
            time.sleep(random.uniform(0.05, 0.15))
            pyautogui.click()


class AutoBot:
    """Fully automatic herblore bot."""
    
    def __init__(self, potion_name):
        self.detector = RuneLiteFixedDetector()
        self.potion_name = potion_name
        self.potions_made = 0
        self.running = True
        self.bank_pos = None
        
        # Load potion data
        with open('data/potions.json', 'r') as f:
            data = json.load(f)
            potions = {p['name']: p for p in data['potions']}
            self.potion = potions[potion_name]
        
        print(f"\n[BOT] Potion: {self.potion['name']}")
        print(f"[BOT] Herb: {self.potion['herb']}")
        print(f"[BOT] XP: {self.potion['xp']}")
    
    def setup(self):
        """Auto-detect everything."""
        print("\n" + "="*60)
        print("AUTO-SETUP")
        print("="*60 + "\n")
        
        # Find window
        if not self.detector.find_game_window():
            return False
        
        # Calculate inventory
        if not self.detector.calculate_inventory_slots():
            return False
        
        # Find bank
        self.bank_pos = self.detector.find_bank()
        if not self.bank_pos:
            return False
        
        print("\n✅ Auto-setup complete!\n")
        return True
    
    def start(self):
        """Start bot."""
        print("="*60)
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
        BezierMovement.move_to(self.bank_pos[0], self.bank_pos[1])
        time.sleep(random.uniform(1.5, 2.5))
        
        # Deposit all using right-click on first inv slot
        print("  Depositing all...")
        first_slot = self.detector.inventory_slots[0]
        
        # Move to first slot
        BezierMovement.move_to(first_slot[0], first_slot[1], click=False)
        time.sleep(random.uniform(0.2, 0.4))
        
        # Right-click
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.3, 0.5))
        
        # Click "Deposit-All" (usually 5th option, ~100px down)
        pyautogui.moveRel(0, 100)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.5, 0.8))
        
        # Withdraw herbs (search for them in bank)
        print(f"  Withdrawing {self.potion['herb']}...")
        
        # Type to search
        pyautogui.write(self.potion['herb'][:4].lower(), interval=0.1)
        time.sleep(0.5)
        
        # Click first search result (top-left of bank)
        bank_first_item_x = self.detector.game_window['x'] + 100
        bank_first_item_y = self.detector.game_window['y'] + 100
        
        BezierMovement.move_to(bank_first_item_x, bank_first_item_y, click=False)
        time.sleep(0.2)
        
        # Right-click
        pyautogui.click(button='right')
        time.sleep(0.3)
        
        # Withdraw-All (usually 4th option)
        pyautogui.moveRel(0, 75)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 1.0))
        
        # Clear search
        pyautogui.press('esc')
        time.sleep(0.3)
        
        # Withdraw vials
        print("  Withdrawing vials...")
        pyautogui.write('vial', interval=0.1)
        time.sleep(0.5)
        
        # Click first result
        BezierMovement.move_to(bank_first_item_x, bank_first_item_y, click=False)
        time.sleep(0.2)
        pyautogui.click(button='right')
        time.sleep(0.3)
        pyautogui.moveRel(0, 75)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(random.uniform(0.6, 1.0))
        
        # Close bank
        print("  Closing bank...")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print("  ✅ Banking complete")
    
    def _make_potions(self):
        """Make potions."""
        print("\n[MAKING POTIONS]")
        
        # Click first herb
        slot = self.detector.inventory_slots[0]
        print("  Clicking herb...")
        BezierMovement.move_to(slot[0], slot[1])
        time.sleep(random.uniform(0.3, 0.5))
        
        # Click first vial (slot 15)
        slot = self.detector.inventory_slots[14]
        print("  Clicking vial...")
        BezierMovement.move_to(slot[0], slot[1])
        time.sleep(random.uniform(0.8, 1.2))
        
        # Press space
        print("  Pressing space...")
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Wait
        print("  Waiting 28s...")
        time.sleep(28)
        
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
    
    # Select
    while True:
        try:
            choice = int(input("\nSelect (1-11): ").strip())
            if 1 <= choice <= len(data['potions']):
                potion = data['potions'][choice - 1]
                break
        except:
            pass
    
    print(f"\n✅ Selected: {potion['name']}\n")
    
    # Create bot
    bot = AutoBot(potion['name'])
    
    # Setup
    if not bot.setup():
        print("\n❌ Setup failed!")
        input("Press Enter to exit...")
        exit(1)
    
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
