#!/usr/bin/env python3
"""
OSRS Herblore Bot - Production Version
Herb + Secondary directly (no vials)
Advanced anti-cheat, state validation, error recovery
"""
import time
import random
import json
import math
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Herblore Bot - PRODUCTION                         ║
║   Advanced Anti-Cheat | State Validation | XP Tracker    ║
╚═══════════════════════════════════════════════════════════╝
""")

# Dependencies
try:
    import pyautogui
    import mss
    import cv2
    from PIL import Image
    print("✅ Ready\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Install: pip install pyautogui mss opencv-python pillow numpy")
    input("Press Enter...")
    exit(1)

pyautogui.FAILSAFE = True


class PotionData:
    """Potion XP data."""
    POTIONS = {
        'Attack potion': {'herb': 'Guam leaf', 'secondary': 'Eye of newt', 'level': 3, 'xp': 25},
        'Strength potion': {'herb': 'Tarromin', 'secondary': 'Limpwurt root', 'level': 12, 'xp': 50},
        'Restore potion': {'herb': 'Harralander', 'secondary': "Red spiders' eggs", 'level': 22, 'xp': 62.5},
        'Prayer potion': {'herb': 'Ranarr weed', 'secondary': 'Snape grass', 'level': 38, 'xp': 87.5},
        'Super attack': {'herb': 'Irit leaf', 'secondary': 'Eye of newt', 'level': 45, 'xp': 100},
        'Super strength': {'herb': 'Kwuarm', 'secondary': 'Limpwurt root', 'level': 55, 'xp': 125},
        'Super restore': {'herb': 'Snapdragon', 'secondary': "Red spiders' eggs", 'level': 63, 'xp': 142.5},
        'Super defence': {'herb': 'Cadantine', 'secondary': 'White berries', 'level': 66, 'xp': 150},
        'Ranging potion': {'herb': 'Dwarf weed', 'secondary': 'Wine of zamorak', 'level': 72, 'xp': 162.5},
    }


class Setup:
    """Setup with template capture."""
    
    def __init__(self):
        self.positions = {}
        self.templates = {}
        self.sct = mss.mss()
        self.potion_data = None
    
    def capture(self, name, instruction):
        """Capture position and template."""
        print(f"\n{'='*60}")
        print(f"CAPTURE: {name}")
        print(f"{'='*60}")
        print(instruction)
        
        input("Press Enter, then move mouse to position...")
        print("Waiting 3 seconds...")
        time.sleep(3)
        
        pos = pyautogui.position()
        x, y = pos.x, pos.y
        
        # Capture template
        region = {'left': x - 25, 'top': y - 25, 'width': 50, 'height': 50}
        screenshot = np.array(self.sct.grab(region))
        
        self.templates[name] = screenshot
        self.positions[name] = (x, y)
        
        # Save
        Path('templates').mkdir(exist_ok=True)
        img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        img.save(f'templates/{name}.png')
        
        print(f"✅ Saved: {name} at ({x}, {y})")
        
        # Confirm
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        if input("Correct? (y/n): ").strip().lower() != 'y':
            return self.capture(name, instruction)
        
        return (x, y)
    
    def run(self):
        """Run setup."""
        print("\n" + "="*60)
        print("SETUP")
        print("="*60)
        
        # Select potion
        print("\nAvailable potions:")
        potions = list(PotionData.POTIONS.keys())
        for i, name in enumerate(potions, 1):
            data = PotionData.POTIONS[name]
            print(f"  {i}. {name} (Lvl {data['level']}, {data['xp']} XP)")
        
        while True:
            try:
                choice = int(input("\nSelect (1-9): "))
                if 1 <= choice <= len(potions):
                    potion_name = potions[choice - 1]
                    self.potion_data = PotionData.POTIONS[potion_name]
                    self.potion_data['name'] = potion_name
                    break
            except:
                pass
        
        print(f"\n✅ {potion_name}")
        print(f"   Herb: {self.potion_data['herb']}")
        print(f"   Secondary: {self.potion_data['secondary']}")
        
        input("\nPress Enter to start setup...")
        
        # Capture positions
        self.capture("bank", "BANK:\nMove mouse to bank booth/chest")
        
        print("\n📋 OPEN the bank")
        input("Press Enter when open...")
        
        # Capture bank interface template
        print("\n[CAPTURE] Bank interface screenshot...")
        bank_region = {'left': 100, 'top': 100, 'width': 600, 'height': 400}
        self.templates['bank_interface'] = np.array(self.sct.grab(bank_region))
        print("✅ Bank interface template saved")
        
        self.capture("deposit", "DEPOSIT BUTTON:\nMove to deposit inventory button")
        self.capture("herb", f"HERB:\nMove to {self.potion_data['herb']} in bank")
        self.capture("secondary", f"SECONDARY:\nMove to {self.potion_data['secondary']} in bank")
        
        print("\n📋 CLOSE bank")
        input("Press Enter when closed...")
        
        self.capture("inv_first", "INVENTORY:\nMove to FIRST inventory slot (top-left)")
        
        # Calculate grid
        x, y = self.positions['inv_first']
        slots = []
        for row in range(7):
            for col in range(4):
                slots.append((x + col * 42, y + row * 36))
        self.positions['inventory_slots'] = slots
        print(f"✅ Calculated {len(slots)} slots")
        
        # Capture Make-X interface template
        print("\n📋 Put herb + secondary in inventory")
        print("📋 Click herb, then secondary to open Make-X")
        input("Press Enter when Make-X interface is showing...")
        
        makex_region = {'left': 200, 'top': 200, 'width': 400, 'height': 300}
        self.templates['makex_interface'] = np.array(self.sct.grab(makex_region))
        print("✅ Make-X interface template saved")
        
        pyautogui.press('esc')
        
        # Save
        self._save()
        
        print("\n✅ Setup complete!")
        return True
    
    def _save(self):
        """Save setup."""
        data = {k: v for k, v in self.positions.items() if k != 'inventory_slots'}
        data['inventory_slots'] = self.positions['inventory_slots']
        data['potion'] = self.potion_data
        
        with open('bot_config.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("📁 Saved: bot_config.json + templates/")
    
    def load(self):
        """Load setup."""
        if not Path('bot_config.json').exists():
            return False
        
        try:
            with open('bot_config.json', 'r') as f:
                data = json.load(f)
                self.positions = {k: v for k, v in data.items() if k not in ['potion']}
                self.potion_data = data['potion']
            
            for file in Path('templates').glob('*.png'):
                name = file.stem
                self.templates[name] = cv2.imread(str(file))
            
            print(f"✅ Loaded: {self.potion_data['name']}")
            return True
        except Exception as e:
            print(f"⚠️  Load failed: {e}")
            return False


class StateValidator:
    """Validate bot state using templates."""
    
    def __init__(self, setup):
        self.setup = setup
        self.sct = mss.mss()
    
    def check_bank_open(self):
        """Check if bank is open."""
        region = {'left': 100, 'top': 100, 'width': 600, 'height': 400}
        screenshot = np.array(self.sct.grab(region))
        
        if 'bank_interface' not in self.setup.templates:
            return True  # Skip if no template
        
        template = self.setup.templates['bank_interface']
        
        # Compare screenshots
        gray_current = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Resize if needed
        if gray_current.shape != gray_template.shape:
            gray_template = cv2.resize(gray_template, (gray_current.shape[1], gray_current.shape[0]))
        
        # Calculate similarity
        diff = cv2.absdiff(gray_current, gray_template)
        similarity = 1 - (np.sum(diff) / (gray_current.size * 255))
        
        is_open = similarity > 0.6
        print(f"  [VALIDATE] Bank open: {'✅' if is_open else '❌'} (similarity: {similarity:.2f})")
        return is_open
    
    def check_makex_interface(self):
        """Check if Make-X interface appeared."""
        region = {'left': 200, 'top': 200, 'width': 400, 'height': 300}
        screenshot = np.array(self.sct.grab(region))
        
        if 'makex_interface' not in self.setup.templates:
            return True
        
        template = self.setup.templates['makex_interface']
        
        gray_current = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        if gray_current.shape != gray_template.shape:
            gray_template = cv2.resize(gray_template, (gray_current.shape[1], gray_current.shape[0]))
        
        diff = cv2.absdiff(gray_current, gray_template)
        similarity = 1 - (np.sum(diff) / (gray_current.size * 255))
        
        is_showing = similarity > 0.6
        print(f"  [VALIDATE] Make-X: {'✅' if is_showing else '❌'} (similarity: {similarity:.2f})")
        return is_showing
    
    def check_inventory_has_items(self):
        """Check if inventory has items (not empty)."""
        first_x, first_y = self.setup.positions['inventory_slots'][0]
        region = {'left': first_x - 10, 'top': first_y - 10, 'width': 200, 'height': 270}
        
        screenshot = np.array(self.sct.grab(region))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Check if mostly dark (empty) or has items
        brightness = gray.mean()
        has_items = brightness > 40  # Items are usually brighter
        
        print(f"  [VALIDATE] Inventory: {'✅ Has items' if has_items else '❌ Empty'} (brightness: {brightness:.1f})")
        return has_items


class AntiCheat:
    """Advanced anti-cheat features."""
    
    @staticmethod
    def move_click(x, y, offset=10):
        """Advanced Bezier movement with anti-detection."""
        start = pyautogui.position()
        
        # Large random offset
        x += random.randint(-offset, offset)
        y += random.randint(-offset, offset)
        
        distance = math.sqrt((x - start[0])**2 + (y - start[1])**2)
        
        # Variable points based on distance
        num_points = random.randint(15, 25) + int(distance / 30)
        
        # Random Bezier control points
        ctrl1_x = start[0] + (x - start[0]) * random.uniform(0.15, 0.35) + random.randint(-50, 50)
        ctrl1_y = start[1] + (y - start[1]) * random.uniform(0.15, 0.35) + random.randint(-50, 50)
        ctrl2_x = start[0] + (x - start[0]) * random.uniform(0.65, 0.85) + random.randint(-50, 50)
        ctrl2_y = start[1] + (y - start[1]) * random.uniform(0.65, 0.85) + random.randint(-50, 50)
        
        # Move with easing
        for i in range(num_points + 1):
            t = i / num_points
            
            # Smooth easing with slight overshoot
            if t < 0.9:
                t_eased = t * t * (3 - 2 * t)
            else:
                t_eased = 1 + (t - 0.9) * 0.5  # Slight overshoot
            
            t_eased = max(0, min(1, t_eased))
            
            px = ((1-t_eased)**3 * start[0] + 3*(1-t_eased)**2*t_eased * ctrl1_x + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_x + t_eased**3 * x)
            py = ((1-t_eased)**3 * start[1] + 3*(1-t_eased)**2*t_eased * ctrl1_y + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_y + t_eased**3 * y)
            
            pyautogui.moveTo(int(px), int(py))
            
            # Variable speed
            if i < 8 or i > num_points - 8:
                delay = random.uniform(0.004, 0.008)
            else:
                delay = random.uniform(0.001, 0.003)
            time.sleep(delay)
        
        # Pre-click pause with variation
        time.sleep(random.uniform(0.09, 0.21))
        
        # Random micro-adjustment
        if random.random() < 0.35:
            pyautogui.moveRel(random.randint(-3, 3), random.randint(-3, 3))
            time.sleep(random.uniform(0.02, 0.06))
        
        # Random hold time
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.02, 0.08))
        pyautogui.mouseUp()
    
    @staticmethod
    def delay(base, variation=0.3):
        """Random delay with Gaussian distribution."""
        delay = random.gauss(base, variation)
        delay = max(0.1, delay)
        time.sleep(delay)


class XPTracker:
    """Track XP and statistics."""
    
    def __init__(self, xp_per_potion):
        self.xp_per_potion = xp_per_potion
        self.potions_made = 0
        self.start_time = datetime.now()
        self.xp_milestones = [1000, 5000, 10000, 50000, 100000]
        self.next_milestone = self.xp_milestones[0] if self.xp_milestones else None
    
    def add_potions(self, count):
        """Add potions and check milestones."""
        self.potions_made += count
        total_xp = self.potions_made * self.xp_per_potion
        
        # Check milestone
        if self.next_milestone and total_xp >= self.next_milestone:
            print(f"\n🎉 MILESTONE: {self.next_milestone:,} XP!")
            # Next milestone
            remaining = [m for m in self.xp_milestones if m > total_xp]
            self.next_milestone = remaining[0] if remaining else None
    
    def get_stats(self):
        """Get current stats."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total_xp = self.potions_made * self.xp_per_potion
        
        if elapsed > 0:
            xp_hour = (total_xp / elapsed) * 3600
            potions_hour = (self.potions_made / elapsed) * 3600
        else:
            xp_hour = 0
            potions_hour = 0
        
        # Estimate to next level (simplified)
        hours_runtime = elapsed / 3600
        
        return {
            'potions': self.potions_made,
            'xp': total_xp,
            'xp_hour': xp_hour,
            'potions_hour': potions_hour,
            'runtime': elapsed,
            'runtime_str': str(timedelta(seconds=int(elapsed)))
        }


class Bot:
    """Main bot with state validation and error recovery."""
    
    def __init__(self, setup):
        self.setup = setup
        self.validator = StateValidator(setup)
        self.xp_tracker = XPTracker(setup.potion_data['xp'])
        self.running = True
        self.max_retries = 3
    
    def start(self):
        """Start bot."""
        print("\n" + "="*60)
        print("BOT STARTING")
        print(f"Potion: {self.setup.potion_data['name']}")
        print(f"XP per potion: {self.setup.potion_data['xp']}")
        print("="*60)
        print("\n⚠️  Move mouse to corner to stop")
        
        input("Press Enter to start...")
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                # Execute with validation
                if not self._bank_with_validation():
                    print("❌ Banking failed after retries - stopping")
                    break
                
                if not self._make_potions_with_validation():
                    print("❌ Potion making failed - stopping")
                    break
                
                # Update stats
                self.xp_tracker.add_potions(14)
                self._print_stats()
                
                # Variable delay with random breaks
                if random.random() < 0.1:  # 10% chance of longer break
                    delay = random.uniform(15, 30)
                    print(f"\n☕ Taking break: {delay:.1f}s...")
                else:
                    delay = random.uniform(5, 10)
                    print(f"\n⏳ Waiting {delay:.1f}s...")
                
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n[BOT] Stopped by user")
        except pyautogui.FailSafeException:
            print("\n[BOT] FAILSAFE triggered")
        finally:
            self._print_final_stats()
    
    def _bank_with_validation(self):
        """Banking with state validation and retries."""
        print("[BANKING]")
        
        for attempt in range(self.max_retries):
            # Open bank
            print(f"  Opening bank... (attempt {attempt + 1})")
            x, y = self.setup.positions['bank']
            AntiCheat.move_click(x, y)
            AntiCheat.delay(2.0, 0.4)
            
            # Validate bank opened
            if not self.validator.check_bank_open():
                print("  ⚠️  Bank didn't open - retrying...")
                continue
            
            # Deposit
            print("  Depositing...")
            x, y = self.setup.positions['deposit']
            AntiCheat.move_click(x, y)
            AntiCheat.delay(0.8, 0.2)
            
            # Withdraw herbs
            print(f"  Withdrawing {self.setup.potion_data['herb']}...")
            x, y = self.setup.positions['herb']
            AntiCheat.move_click(x, y)
            AntiCheat.delay(0.4, 0.1)
            
            pyautogui.click(button='right')
            AntiCheat.delay(0.4, 0.1)
            
            pyautogui.moveRel(random.randint(-2, 2), random.randint(38, 42))
            AntiCheat.delay(0.15, 0.05)
            pyautogui.click()
            AntiCheat.delay(0.8, 0.2)
            
            # Withdraw secondary
            print(f"  Withdrawing {self.setup.potion_data['secondary']}...")
            x, y = self.setup.positions['secondary']
            AntiCheat.move_click(x, y)
            AntiCheat.delay(0.4, 0.1)
            
            pyautogui.click(button='right')
            AntiCheat.delay(0.4, 0.1)
            
            pyautogui.moveRel(random.randint(-2, 2), random.randint(38, 42))
            AntiCheat.delay(0.15, 0.05)
            pyautogui.click()
            AntiCheat.delay(0.8, 0.2)
            
            # Close bank
            print("  Closing bank...")
            pyautogui.press('esc')
            AntiCheat.delay(0.6, 0.2)
            
            # Validate inventory has items
            if not self.validator.check_inventory_has_items():
                print("  ⚠️  Inventory empty - retrying...")
                continue
            
            print("  ✅ Banking done")
            return True
        
        return False
    
    def _make_potions_with_validation(self):
        """Make potions with validation."""
        print("\n[MAKING POTIONS]")
        
        for attempt in range(self.max_retries):
            slots = self.setup.positions['inventory_slots']
            
            # Click herb
            print(f"  Clicking herb... (attempt {attempt + 1})")
            x, y = slots[0]
            AntiCheat.move_click(x, y)
            AntiCheat.delay(0.4, 0.1)
            
            # Click secondary
            print("  Clicking secondary...")
            x, y = slots[14]
            AntiCheat.move_click(x, y)
            AntiCheat.delay(1.2, 0.3)
            
            # Validate Make-X appeared
            if not self.validator.check_makex_interface():
                print("  ⚠️  Make-X didn't appear - retrying...")
                pyautogui.press('esc')
                AntiCheat.delay(0.5, 0.1)
                continue
            
            # Start making
            print("  Pressing space...")
            pyautogui.press('space')
            AntiCheat.delay(0.6, 0.2)
            
            # Wait for completion
            wait = random.uniform(16, 20)
            print(f"  Waiting {wait:.1f}s...")
            time.sleep(wait)
            
            print("  ✅ Potions made")
            return True
        
        return False
    
    def _print_stats(self):
        """Print current stats."""
        stats = self.xp_tracker.get_stats()
        
        print(f"\n📊 STATS:")
        print(f"   Potions: {stats['potions']:,}")
        print(f"   Total XP: {stats['xp']:,.0f}")
        print(f"   XP/hour: {stats['xp_hour']:,.0f}")
        print(f"   Potions/hour: {stats['potions_hour']:.1f}")
        print(f"   Runtime: {stats['runtime_str']}")
    
    def _print_final_stats(self):
        """Print final stats."""
        print("\n" + "="*60)
        print("FINAL STATS")
        print("="*60)
        
        stats = self.xp_tracker.get_stats()
        
        print(f"Potions made: {stats['potions']:,}")
        print(f"Total XP: {stats['xp']:,.0f}")
        print(f"Average XP/hour: {stats['xp_hour']:,.0f}")
        print(f"Total runtime: {stats['runtime_str']}")
        print("="*60)


def main():
    """Main."""
    setup = Setup()
    
    if setup.load():
        if input("\nReuse setup? (y/n): ").strip().lower() != 'y':
            setup.run()
    else:
        setup.run()
    
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
