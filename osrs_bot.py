#!/usr/bin/env python3
"""
OSRS Herblore Bot - Production v2
- Misclick detection via template matching
- Single-click withdraws (Shift+Click)
- Visual feedback on validation checks
- Complete recipe system
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
║   OSRS Herblore Bot v2                                    ║
║   Misclick Detection | Visual Validation | 1-Click        ║
╚═══════════════════════════════════════════════════════════╝
""")

try:
    import pyautogui
    import mss
    import cv2
    from PIL import Image, ImageDraw, ImageFont
    print("✅ Ready\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    input("Press Enter...")
    exit(1)

pyautogui.FAILSAFE = True


class PotionRecipes:
    """Complete potion recipe database."""
    RECIPES = {
        'Attack potion': {'herb': 'Guam leaf', 'secondary': 'Eye of newt', 'level': 3, 'xp': 25},
        'Antipoison': {'herb': 'Marrentill', 'secondary': 'Unicorn horn dust', 'level': 5, 'xp': 37.5},
        'Strength potion': {'herb': 'Tarromin', 'secondary': 'Limpwurt root', 'level': 12, 'xp': 50},
        'Restore potion': {'herb': 'Harralander', 'secondary': "Red spiders' eggs", 'level': 22, 'xp': 62.5},
        'Energy potion': {'herb': 'Harralander', 'secondary': 'Chocolate dust', 'level': 26, 'xp': 67.5},
        'Prayer potion': {'herb': 'Ranarr weed', 'secondary': 'Snape grass', 'level': 38, 'xp': 87.5},
        'Super attack': {'herb': 'Irit leaf', 'secondary': 'Eye of newt', 'level': 45, 'xp': 100},
        'Super strength': {'herb': 'Kwuarm', 'secondary': 'Limpwurt root', 'level': 55, 'xp': 125},
        'Super restore': {'herb': 'Snapdragon', 'secondary': "Red spiders' eggs", 'level': 63, 'xp': 142.5},
        'Super defence': {'herb': 'Cadantine', 'secondary': 'White berries', 'level': 66, 'xp': 150},
        'Ranging potion': {'herb': 'Dwarf weed', 'secondary': 'Wine of zamorak', 'level': 72, 'xp': 162.5},
        'Saradomin brew': {'herb': 'Toadflax', 'secondary': 'Crushed nest', 'level': 81, 'xp': 180},
    }


class Setup:
    """Setup with enhanced template capture."""
    
    def __init__(self):
        self.positions = {}
        self.templates = {}
        self.sct = mss.mss()
        self.potion_data = None
    
    def capture(self, name, instruction):
        """Capture position with larger template."""
        print(f"\n{'='*60}")
        print(f"CAPTURE: {name}")
        print(f"{'='*60}")
        print(instruction)
        
        input("Press Enter, move mouse to position...")
        print("Waiting 3 seconds...")
        time.sleep(3)
        
        pos = pyautogui.position()
        x, y = pos.x, pos.y
        
        # Capture larger template for better matching
        region = {'left': x - 30, 'top': y - 30, 'width': 60, 'height': 60}
        screenshot = np.array(self.sct.grab(region))
        
        self.templates[name] = screenshot
        self.positions[name] = (x, y)
        
        # Save template
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
        
        # Show recipes
        print("\nAvailable potions:")
        recipes = list(PotionRecipes.RECIPES.keys())
        for i, name in enumerate(recipes, 1):
            data = PotionRecipes.RECIPES[name]
            print(f"  {i:2d}. {name:<20} Lvl {data['level']:2d} | {data['xp']:5.1f} XP")
            print(f"      {data['herb']} + {data['secondary']}")
        
        while True:
            try:
                choice = int(input("\nSelect (1-12): "))
                if 1 <= choice <= len(recipes):
                    potion_name = recipes[choice - 1]
                    self.potion_data = PotionRecipes.RECIPES[potion_name].copy()
                    self.potion_data['name'] = potion_name
                    break
            except:
                pass
        
        print(f"\n✅ {potion_name}")
        print(f"   {self.potion_data['herb']} + {self.potion_data['secondary']}")
        
        input("\nPress Enter to start setup...")
        
        # Capture positions
        self.capture("bank", "BANK:\nMove to bank booth/chest")
        
        print("\n📋 OPEN the bank")
        input("Press Enter when open...")
        
        self.capture("deposit", "DEPOSIT:\nMove to deposit inventory button")
        self.capture("herb", f"HERB:\nMove to {self.potion_data['herb']} in bank")
        self.capture("secondary", f"SECONDARY:\nMove to {self.potion_data['secondary']}")
        
        print("\n📋 CLOSE bank")
        input("Press Enter when closed...")
        
        self.capture("inv_first", "INVENTORY:\nMove to first slot (top-left)")
        
        # Grid
        x, y = self.positions['inv_first']
        slots = [(x + col * 42, y + row * 36) for row in range(7) for col in range(4)]
        self.positions['inventory_slots'] = slots
        print(f"✅ {len(slots)} slots calculated")
        
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
        
        print("📁 Saved: bot_config.json")
    
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


class Validator:
    """Enhanced validator with visual feedback."""
    
    def __init__(self, setup):
        self.setup = setup
        self.sct = mss.mss()
        Path('validation_checks').mkdir(exist_ok=True)
    
    def check_clicked_correct_item(self, item_name, click_pos):
        """Verify we clicked the correct item by template matching."""
        print(f"  [VALIDATE] Checking if {item_name} was clicked...")
        
        if item_name not in self.setup.templates:
            print(f"  ⚠️  No template for {item_name}")
            return True
        
        # Capture area around click
        x, y = click_pos
        region = {'left': x - 30, 'top': y - 30, 'width': 60, 'height': 60}
        screenshot = np.array(self.sct.grab(region))
        
        # Compare with template
        template = self.setup.templates[item_name]
        
        # Ensure same size
        if screenshot.shape != template.shape:
            template = cv2.resize(template, (screenshot.shape[1], screenshot.shape[0]))
        
        # Calculate similarity
        gray_current = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(gray_current, gray_template)
        similarity = 1 - (np.sum(diff) / (gray_current.size * 255))
        
        # Save visual comparison
        self._save_comparison(item_name, screenshot, template, similarity)
        
        passed = similarity > 0.65
        status = "✅" if passed else "❌"
        print(f"  {status} {item_name} match: {similarity:.2f}")
        
        return passed
    
    def _save_comparison(self, name, current, template, score):
        """Save visual comparison image."""
        # Create side-by-side comparison
        h, w = current.shape[:2]
        comparison = np.zeros((h, w * 2 + 10, 3), dtype=np.uint8)
        comparison[:, :w] = current
        comparison[:, w+10:] = template
        
        # Convert for PIL
        img = Image.fromarray(cv2.cvtColor(comparison, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = f"{name} | Score: {score:.2f} | {'PASS' if score > 0.65 else 'FAIL'}"
        draw.text((10, 10), text, fill=(255, 255, 0))
        
        timestamp = datetime.now().strftime("%H%M%S")
        img.save(f'validation_checks/{name}_{timestamp}.png')
        print(f"  📸 Saved: validation_checks/{name}_{timestamp}.png")


class Movement:
    """Anti-cheat movement."""
    
    @staticmethod
    def move_click(x, y, offset=10):
        """Smooth Bezier with anti-cheat."""
        start = pyautogui.position()
        
        x += random.randint(-offset, offset)
        y += random.randint(-offset, offset)
        
        distance = math.sqrt((x - start[0])**2 + (y - start[1])**2)
        num_points = random.randint(15, 25) + int(distance / 30)
        
        ctrl1_x = start[0] + (x - start[0]) * random.uniform(0.15, 0.35) + random.randint(-50, 50)
        ctrl1_y = start[1] + (y - start[1]) * random.uniform(0.15, 0.35) + random.randint(-50, 50)
        ctrl2_x = start[0] + (x - start[0]) * random.uniform(0.65, 0.85) + random.randint(-50, 50)
        ctrl2_y = start[1] + (y - start[1]) * random.uniform(0.65, 0.85) + random.randint(-50, 50)
        
        for i in range(num_points + 1):
            t = i / num_points
            t_eased = t * t * (3 - 2 * t) if t < 0.9 else 1 + (t - 0.9) * 0.5
            t_eased = max(0, min(1, t_eased))
            
            px = ((1-t_eased)**3 * start[0] + 3*(1-t_eased)**2*t_eased * ctrl1_x + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_x + t_eased**3 * x)
            py = ((1-t_eased)**3 * start[1] + 3*(1-t_eased)**2*t_eased * ctrl1_y + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_y + t_eased**3 * y)
            
            pyautogui.moveTo(int(px), int(py))
            delay = random.uniform(0.004, 0.008) if i < 8 or i > num_points - 8 else random.uniform(0.001, 0.003)
            time.sleep(delay)
        
        time.sleep(random.uniform(0.09, 0.21))
        
        if random.random() < 0.35:
            pyautogui.moveRel(random.randint(-3, 3), random.randint(-3, 3))
            time.sleep(random.uniform(0.02, 0.06))
        
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.02, 0.08))
        pyautogui.mouseUp()
    
    @staticmethod
    def delay(base, variation=0.3):
        """Gaussian delay."""
        delay = random.gauss(base, variation)
        time.sleep(max(0.1, delay))


class XPTracker:
    """XP tracking."""
    
    def __init__(self, xp_per):
        self.xp_per = xp_per
        self.potions = 0
        self.start = datetime.now()
        self.milestones = [1000, 5000, 10000, 50000, 100000]
        self.next = self.milestones[0] if self.milestones else None
    
    def add(self, count):
        """Add potions."""
        self.potions += count
        xp = self.potions * self.xp_per
        
        if self.next and xp >= self.next:
            print(f"\n🎉 {self.next:,} XP!")
            remaining = [m for m in self.milestones if m > xp]
            self.next = remaining[0] if remaining else None
    
    def stats(self):
        """Get stats."""
        elapsed = (datetime.now() - self.start).total_seconds()
        xp = self.potions * self.xp_per
        xp_hour = (xp / elapsed) * 3600 if elapsed > 0 else 0
        
        return {
            'potions': self.potions,
            'xp': xp,
            'xp_hour': xp_hour,
            'runtime': str(timedelta(seconds=int(elapsed)))
        }


class Bot:
    """Main bot with misclick detection."""
    
    def __init__(self, setup):
        self.setup = setup
        self.validator = Validator(setup)
        self.xp = XPTracker(setup.potion_data['xp'])
        self.running = True
        self.max_retries = 3
    
    def start(self):
        """Start."""
        print("\n" + "="*60)
        print(f"BOT: {self.setup.potion_data['name']}")
        print(f"XP: {self.setup.potion_data['xp']} per potion")
        print("="*60)
        print("\n⚠️  Validation images saved to: validation_checks/")
        print("⚠️  Move mouse to corner to stop")
        
        input("Press Enter...")
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                if not self._bank():
                    print("❌ Banking failed")
                    break
                
                if not self._make():
                    print("❌ Making failed")
                    break
                
                self.xp.add(14)
                self._stats()
                
                delay = random.uniform(15, 30) if random.random() < 0.1 else random.uniform(5, 10)
                print(f"\n⏳ {delay:.1f}s...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n[STOPPED]")
        except pyautogui.FailSafeException:
            print("\n[FAILSAFE]")
        finally:
            stats = self.xp.stats()
            print(f"\n{'='*60}")
            print(f"FINAL: {stats['potions']:,} potions | {stats['xp']:,.0f} XP")
            print(f"Runtime: {stats['runtime']}")
            print(f"{'='*60}")
    
    def _bank(self):
        """Banking with validation."""
        print("[BANKING]")
        
        for attempt in range(self.max_retries):
            # Open
            print(f"  Opening... (attempt {attempt + 1})")
            x, y = self.setup.positions['bank']
            Movement.move_click(x, y)
            Movement.delay(2.0, 0.4)
            
            # Validate we clicked bank
            if not self.validator.check_clicked_correct_item('bank', (x, y)):
                print("  ⚠️  Misclick - retrying...")
                continue
            
            # Deposit
            print("  Depositing...")
            x, y = self.setup.positions['deposit']
            Movement.move_click(x, y)
            Movement.delay(0.8, 0.2)
            
            # Withdraw herbs (SHIFT+CLICK for Withdraw-All)
            print(f"  Withdrawing {self.setup.potion_data['herb']}...")
            x, y = self.setup.positions['herb']
            
            # Hold shift and click
            pyautogui.keyDown('shift')
            Movement.move_click(x, y)
            pyautogui.keyUp('shift')
            Movement.delay(0.8, 0.2)
            
            # Validate herb clicked
            if not self.validator.check_clicked_correct_item('herb', (x, y)):
                print("  ⚠️  Herb misclick - retrying...")
                pyautogui.press('esc')
                continue
            
            # Withdraw secondary (SHIFT+CLICK)
            print(f"  Withdrawing {self.setup.potion_data['secondary']}...")
            x, y = self.setup.positions['secondary']
            
            pyautogui.keyDown('shift')
            Movement.move_click(x, y)
            pyautogui.keyUp('shift')
            Movement.delay(0.8, 0.2)
            
            # Validate secondary clicked
            if not self.validator.check_clicked_correct_item('secondary', (x, y)):
                print("  ⚠️  Secondary misclick - retrying...")
                pyautogui.press('esc')
                continue
            
            # Close
            print("  Closing...")
            pyautogui.press('esc')
            Movement.delay(0.6, 0.2)
            
            print("  ✅ Done")
            return True
        
        return False
    
    def _make(self):
        """Make potions."""
        print("\n[MAKING]")
        
        for attempt in range(self.max_retries):
            slots = self.setup.positions['inventory_slots']
            
            # Herb
            print(f"  Herb... (attempt {attempt + 1})")
            x, y = slots[0]
            Movement.move_click(x, y)
            Movement.delay(0.4, 0.1)
            
            # Secondary
            print("  Secondary...")
            x, y = slots[14]
            Movement.move_click(x, y)
            Movement.delay(1.2, 0.3)
            
            # Space
            print("  Space...")
            pyautogui.press('space')
            Movement.delay(0.6, 0.2)
            
            # Wait
            wait = random.uniform(16, 20)
            print(f"  Waiting {wait:.1f}s...")
            time.sleep(wait)
            
            print("  ✅ Done")
            return True
        
        return False
    
    def _stats(self):
        """Print stats."""
        s = self.xp.stats()
        print(f"\n📊 {s['potions']:,} potions | {s['xp']:,.0f} XP | {s['xp_hour']:,.0f}/hr | {s['runtime']}")


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
        print(f"\n❌ {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter...")
