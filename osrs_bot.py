#!/usr/bin/env python3
"""
OSRS Herblore Bot - Production v3
- Enhanced anti-ban with position variance
- Smoother mouse movements
- Better setup flow with secondary validation
- Configuration persistence
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
║   OSRS Herblore Bot v3                                    ║
║   Anti-Ban++ | Smooth Movement | Position Variance        ║
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
    """Enhanced setup with detailed validation."""
    
    def __init__(self):
        self.positions = {}
        self.templates = {}
        self.sct = mss.mss()
        self.potion_data = None
    
    def capture(self, name, instruction, highlight_color=None):
        """Capture position with visual feedback."""
        print(f"\n{'='*60}")
        print(f"STEP: {name.upper()}")
        print(f"{'='*60}")
        print(instruction)
        
        if highlight_color:
            print(f"🎯 Look for: {highlight_color}")
        
        input("\n👉 Press Enter, then move mouse to position...")
        print("⏳ Waiting 3 seconds...")
        time.sleep(3)
        
        pos = pyautogui.position()
        x, y = pos.x, pos.y
        
        # Capture larger template (70x70 for better matching)
        region = {'left': x - 35, 'top': y - 35, 'width': 70, 'height': 70}
        screenshot = np.array(self.sct.grab(region))
        
        # Convert BGRA to BGR
        if screenshot.shape[2] == 4:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        self.templates[name] = screenshot
        self.positions[name] = (x, y)
        
        # Save template
        Path('templates').mkdir(exist_ok=True)
        img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        img.save(f'templates/{name}.png')
        
        print(f"✅ Captured: {name} at ({x}, {y})")
        
        # Visual confirmation
        pyautogui.moveTo(x, y)
        time.sleep(0.3)
        
        # Draw circle at position (visual feedback)
        for radius in range(5, 25, 5):
            for angle in range(0, 360, 15):
                offset_x = int(radius * math.cos(math.radians(angle)))
                offset_y = int(radius * math.sin(math.radians(angle)))
                pyautogui.moveTo(x + offset_x, y + offset_y, duration=0.05)
        
        pyautogui.moveTo(x, y)
        
        if input("✓ Correct position? (y/n): ").strip().lower() != 'y':
            return self.capture(name, instruction, highlight_color)
        
        return (x, y)
    
    def run(self):
        """Run enhanced setup."""
        print("\n" + "="*60)
        print("🔧 SETUP WIZARD")
        print("="*60)
        
        # Show recipes
        print("\n📋 Available potions:")
        recipes = list(PotionRecipes.RECIPES.keys())
        for i, name in enumerate(recipes, 1):
            data = PotionRecipes.RECIPES[name]
            print(f"  {i:2d}. {name:<20} Lvl {data['level']:2d} | {data['xp']:5.1f} XP")
            print(f"      🌿 {data['herb']}")
            print(f"      🧪 {data['secondary']}")
        
        while True:
            try:
                choice = int(input("\n👉 Select potion (1-12): "))
                if 1 <= choice <= len(recipes):
                    potion_name = recipes[choice - 1]
                    self.potion_data = PotionRecipes.RECIPES[potion_name].copy()
                    self.potion_data['name'] = potion_name
                    break
            except:
                pass
        
        print(f"\n✅ Selected: {potion_name}")
        print(f"   🌿 Herb: {self.potion_data['herb']}")
        print(f"   🧪 Secondary: {self.potion_data['secondary']}")
        print(f"   📊 {self.potion_data['xp']} XP per potion")
        
        input("\n👉 Press Enter to begin setup...")
        
        # Step 1: Bank
        self.capture(
            "bank",
            "📍 BANK BOOTH/CHEST:\n"
            "Move your mouse over the bank booth or chest.\n"
            "This is where the bot will click to open the bank.",
            "Brown/Gray structure"
        )
        
        # Step 2: Open bank
        print("\n" + "="*60)
        print("⚠️  OPEN THE BANK NOW")
        print("="*60)
        print("Click the bank booth/chest to open your bank.")
        input("Press Enter when bank is open...")
        
        # Step 3: Deposit button
        self.capture(
            "deposit",
            "📍 DEPOSIT INVENTORY BUTTON:\n"
            "Move your mouse over the 'Deposit Inventory' button.\n"
            "Usually at the bottom-right of the bank interface.",
            "Red/Orange button"
        )
        
        # Step 4: Herb
        self.capture(
            "herb",
            f"📍 HERB IN BANK:\n"
            f"Move your mouse over '{self.potion_data['herb']}'.\n"
            f"Make sure you have this herb in your bank!\n"
            f"The bot will Shift+Click here to withdraw.",
            f"🌿 {self.potion_data['herb']}"
        )
        
        # Step 5: Secondary
        print("\n" + "="*60)
        print("🧪 IMPORTANT: SECONDARY INGREDIENT")
        print("="*60)
        print(f"Next, you'll select where '{self.potion_data['secondary']}' is.")
        print("This is the ingredient you combine WITH the herb.")
        print(f"Example: {self.potion_data['herb']} + {self.potion_data['secondary']} = {potion_name}")
        
        self.capture(
            "secondary",
            f"📍 SECONDARY IN BANK:\n"
            f"Move your mouse over '{self.potion_data['secondary']}'.\n"
            f"This must be in your bank!\n"
            f"The bot will Shift+Click here to withdraw.",
            f"🧪 {self.potion_data['secondary']}"
        )
        
        # Step 6: Close bank
        print("\n" + "="*60)
        print("⚠️  CLOSE THE BANK NOW")
        print("="*60)
        print("Press ESC or click the X to close the bank.")
        input("Press Enter when bank is closed...")
        
        # Step 7: First inventory slot
        self.capture(
            "inv_first",
            "📍 FIRST INVENTORY SLOT:\n"
            "Move your mouse over the FIRST slot (top-left) of your inventory.\n"
            "The bot will calculate all 28 slots from this position.",
            "Top-left empty slot"
        )
        
        # Calculate inventory grid
        x, y = self.positions['inv_first']
        slots = [(x + col * 42, y + row * 36) for row in range(7) for col in range(4)]
        self.positions['inventory_slots'] = slots
        print(f"✅ Calculated {len(slots)} inventory slots")
        
        # Show slot positions
        print("\n📊 Inventory Grid Preview:")
        print("   Slot 0-13: Herbs will appear here")
        print("   Slot 14-27: Secondaries will appear here")
        
        # Save everything
        self._save()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print(f"📁 Configuration saved to: bot_config.json")
        print(f"📁 Templates saved to: templates/")
        print(f"\n🎯 Bot will make: {potion_name}")
        print(f"   🌿 {self.potion_data['herb']} (Shift+Click from bank)")
        print(f"   🧪 {self.potion_data['secondary']} (Shift+Click from bank)")
        print(f"   📊 {self.potion_data['xp']} XP per potion")
        
        return True
    
    def _save(self):
        """Save setup to configuration file."""
        config = {
            'version': 3,
            'created': datetime.now().isoformat(),
            'potion': self.potion_data,
            'positions': {
                'bank': self.positions['bank'],
                'deposit': self.positions['deposit'],
                'herb': self.positions['herb'],
                'secondary': self.positions['secondary'],
                'inv_first': self.positions['inv_first'],
                'inventory_slots': self.positions['inventory_slots']
            },
            'notes': {
                'herb': f"Shift+Click to withdraw {self.potion_data['herb']}",
                'secondary': f"Shift+Click to withdraw {self.potion_data['secondary']}",
                'inventory': "Calculated 28-slot grid (4 cols × 7 rows, 42×36 spacing)"
            }
        }
        
        with open('bot_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("💾 Configuration saved")
    
    def load(self):
        """Load setup from configuration file."""
        if not Path('bot_config.json').exists():
            return False
        
        try:
            with open('bot_config.json', 'r') as f:
                config = json.load(f)
            
            # Load positions
            self.positions = config['positions']
            self.potion_data = config['potion']
            
            # Load templates
            for file in Path('templates').glob('*.png'):
                name = file.stem
                img = cv2.imread(str(file))
                if img is not None:
                    self.templates[name] = img
            
            print(f"✅ Loaded configuration:")
            print(f"   🎯 Potion: {self.potion_data['name']}")
            print(f"   🌿 Herb: {self.potion_data['herb']}")
            print(f"   🧪 Secondary: {self.potion_data['secondary']}")
            print(f"   📊 {self.potion_data['xp']} XP per potion")
            print(f"   📅 Created: {config.get('created', 'Unknown')}")
            
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
        """Verify we clicked the correct item."""
        print(f"  [VALIDATE] Checking {item_name}...")
        
        if item_name not in self.setup.templates:
            print(f"  ⚠️  No template for {item_name}")
            return True
        
        # Capture area around click
        x, y = click_pos
        region = {'left': x - 35, 'top': y - 35, 'width': 70, 'height': 70}
        screenshot = np.array(self.sct.grab(region))
        
        # Convert BGRA to BGR
        if screenshot.shape[2] == 4:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        # Compare with template
        template = self.setup.templates[item_name]
        
        # Convert BGRA to BGR if needed
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
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
        print(f"  {status} {item_name}: {similarity:.2f}")
        
        return passed
    
    def _save_comparison(self, name, current, template, score):
        """Save visual comparison image."""
        # Convert BGRA to BGR if needed
        if current.shape[2] == 4:
            current = cv2.cvtColor(current, cv2.COLOR_BGRA2BGR)
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
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


class Movement:
    """Enhanced anti-cheat movement system."""
    
    # Track recent positions to avoid repetition
    recent_positions = []
    max_history = 10
    
    @staticmethod
    def get_varied_position(base_x, base_y, variance=15):
        """Get varied click position that hasn't been used recently."""
        attempts = 0
        max_attempts = 20
        
        while attempts < max_attempts:
            # Random offset (±variance pixels)
            offset_x = random.randint(-variance, variance)
            offset_y = random.randint(-variance, variance)
            
            new_x = base_x + offset_x
            new_y = base_y + offset_y
            
            # Check if too close to recent positions
            too_close = False
            for old_x, old_y in Movement.recent_positions:
                distance = math.sqrt((new_x - old_x)**2 + (new_y - old_y)**2)
                if distance < 8:  # Minimum 8 pixels apart
                    too_close = True
                    break
            
            if not too_close:
                # Good position, use it
                Movement.recent_positions.append((new_x, new_y))
                if len(Movement.recent_positions) > Movement.max_history:
                    Movement.recent_positions.pop(0)
                return (new_x, new_y)
            
            attempts += 1
        
        # Fallback: just use the varied position
        return (base_x + offset_x, base_y + offset_y)
    
    @staticmethod
    def move_click(x, y, offset=15):
        """Enhanced smooth Bezier movement with anti-cheat."""
        start = pyautogui.position()
        
        # Get varied position (never clicks same spot twice)
        x, y = Movement.get_varied_position(x, y, offset)
        
        distance = math.sqrt((x - start[0])**2 + (y - start[1])**2)
        
        # More points = smoother (25-40 points based on distance)
        num_points = random.randint(25, 35) + int(distance / 20)
        
        # Enhanced control points with more randomness
        ctrl1_x = start[0] + (x - start[0]) * random.uniform(0.20, 0.35) + random.randint(-60, 60)
        ctrl1_y = start[1] + (y - start[1]) * random.uniform(0.20, 0.35) + random.randint(-60, 60)
        ctrl2_x = start[0] + (x - start[0]) * random.uniform(0.65, 0.80) + random.randint(-60, 60)
        ctrl2_y = start[1] + (y - start[1]) * random.uniform(0.65, 0.80) + random.randint(-60, 60)
        
        # Optional: Add slight curve to path (human deviation)
        if random.random() < 0.3:
            ctrl1_x += random.randint(-30, 30)
            ctrl2_y += random.randint(-30, 30)
        
        for i in range(num_points + 1):
            t = i / num_points
            
            # Enhanced easing with slight overshoot
            if t < 0.05:
                # Very slow start
                t_eased = t * t * 0.5
            elif t < 0.92:
                # Smooth middle with slight acceleration
                t_eased = t * t * (3 - 2 * t)
            else:
                # Slight overshoot then settle
                overshoot = (t - 0.92) * 2
                t_eased = 0.92 + overshoot * (1.1 if random.random() < 0.5 else 1.05)
            
            t_eased = max(0, min(1, t_eased))
            
            # Cubic Bezier
            px = ((1-t_eased)**3 * start[0] + 3*(1-t_eased)**2*t_eased * ctrl1_x + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_x + t_eased**3 * x)
            py = ((1-t_eased)**3 * start[1] + 3*(1-t_eased)**2*t_eased * ctrl1_y + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_y + t_eased**3 * y)
            
            # Add micro-jitter (human hand tremor)
            if random.random() < 0.15 and i > 5:
                px += random.uniform(-0.5, 0.5)
                py += random.uniform(-0.5, 0.5)
            
            pyautogui.moveTo(int(px), int(py))
            
            # Variable speed throughout
            if i < 5 or i > num_points - 5:
                delay = random.uniform(0.005, 0.012)  # Slower at start/end
            elif random.random() < 0.1:
                delay = random.uniform(0.008, 0.015)  # Occasional hesitation
            else:
                delay = random.uniform(0.001, 0.004)  # Fast middle
            
            time.sleep(delay)
        
        # Pause before click (human reaction time)
        time.sleep(random.uniform(0.08, 0.18))
        
        # Micro-adjustment before click (40% chance)
        if random.random() < 0.40:
            adjust_x = random.randint(-2, 2)
            adjust_y = random.randint(-2, 2)
            pyautogui.moveRel(adjust_x, adjust_y)
            time.sleep(random.uniform(0.02, 0.05))
        
        # Click with variable hold time
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.025, 0.095))
        pyautogui.mouseUp()
        
        # Occasional post-click micro-movement (20% chance)
        if random.random() < 0.20:
            time.sleep(random.uniform(0.01, 0.03))
            pyautogui.moveRel(random.randint(-3, 3), random.randint(-3, 3))
    
    @staticmethod
    def delay(base, variation=0.3):
        """Gaussian delay with occasional longer pauses."""
        # 5% chance of distraction (longer delay)
        if random.random() < 0.05:
            delay = random.uniform(base * 1.5, base * 2.5)
            print(f"  💤 Distraction ({delay:.1f}s)...")
        else:
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
            print(f"\n🎉 Milestone: {self.next:,} XP!")
            remaining = [m for m in self.milestones if m > xp]
            self.next = remaining[0] if remaining else None
    
    def stats(self):
        """Get stats."""
        elapsed = (datetime.now() - self.start).total_seconds()
        xp = self.potions * self.xp_per
        xp_hour = (xp / elapsed) * 3600 if elapsed > 0 else 0
        potions_hour = (self.potions / elapsed) * 3600 if elapsed > 0 else 0
        
        return {
            'potions': self.potions,
            'xp': xp,
            'xp_hour': xp_hour,
            'potions_hour': potions_hour,
            'runtime': str(timedelta(seconds=int(elapsed)))
        }


class Bot:
    """Main bot with enhanced anti-ban."""
    
    def __init__(self, setup):
        self.setup = setup
        self.validator = Validator(setup)
        self.xp = XPTracker(setup.potion_data['xp'])
        self.running = True
        self.max_retries = 3
    
    def start(self):
        """Start."""
        print("\n" + "="*60)
        print(f"🤖 BOT STARTING")
        print("="*60)
        print(f"🎯 Potion: {self.setup.potion_data['name']}")
        print(f"🌿 Herb: {self.setup.potion_data['herb']}")
        print(f"🧪 Secondary: {self.setup.potion_data['secondary']}")
        print(f"📊 XP: {self.setup.potion_data['xp']} per potion")
        print("="*60)
        print("\n⚠️  Position variance: ±15 pixels (anti-cheat)")
        print("⚠️  Validation: Templates saved to validation_checks/")
        print("⚠️  Move mouse to corner to stop")
        
        input("\n👉 Press Enter to start...")
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"🔄 ITERATION #{iteration}")
                print(f"{'='*60}\n")
                
                if not self._bank():
                    print("❌ Banking failed")
                    break
                
                if not self._make():
                    print("❌ Making failed")
                    break
                
                self.xp.add(14)
                self._stats()
                
                # Random break chance
                delay = random.uniform(15, 30) if random.random() < 0.15 else random.uniform(6, 11)
                print(f"\n⏳ Break: {delay:.1f}s...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n⚠️  Stopped by user")
        except pyautogui.FailSafeException:
            print("\n⚠️  Failsafe triggered")
        finally:
            stats = self.xp.stats()
            print(f"\n{'='*60}")
            print(f"📊 FINAL STATS")
            print(f"{'='*60}")
            print(f"Potions: {stats['potions']:,}")
            print(f"XP: {stats['xp']:,.0f}")
            print(f"XP/hour: {stats['xp_hour']:,.0f}")
            print(f"Potions/hour: {stats['potions_hour']:,.0f}")
            print(f"Runtime: {stats['runtime']}")
            print(f"{'='*60}")
    
    def _bank(self):
        """Banking with validation."""
        print("🏦 [BANKING]")
        
        for attempt in range(self.max_retries):
            # Open
            print(f"  Opening bank... (attempt {attempt + 1}/{self.max_retries})")
            x, y = self.setup.positions['bank']
            Movement.move_click(x, y)
            Movement.delay(2.0, 0.4)
            
            # Validate
            if not self.validator.check_clicked_correct_item('bank', (x, y)):
                print("  ⚠️  Bank misclick - retrying...")
                continue
            
            # Deposit
            print("  Depositing inventory...")
            x, y = self.setup.positions['deposit']
            Movement.move_click(x, y)
            Movement.delay(0.8, 0.2)
            
            # Withdraw herbs
            print(f"  Withdrawing {self.setup.potion_data['herb']}...")
            x, y = self.setup.positions['herb']
            
            pyautogui.keyDown('shift')
            Movement.move_click(x, y)
            pyautogui.keyUp('shift')
            Movement.delay(0.8, 0.2)
            
            if not self.validator.check_clicked_correct_item('herb', (x, y)):
                print("  ⚠️  Herb misclick - retrying...")
                pyautogui.press('esc')
                continue
            
            # Withdraw secondary
            print(f"  Withdrawing {self.setup.potion_data['secondary']}...")
            x, y = self.setup.positions['secondary']
            
            pyautogui.keyDown('shift')
            Movement.move_click(x, y)
            pyautogui.keyUp('shift')
            Movement.delay(0.8, 0.2)
            
            if not self.validator.check_clicked_correct_item('secondary', (x, y)):
                print("  ⚠️  Secondary misclick - retrying...")
                pyautogui.press('esc')
                continue
            
            # Close
            print("  Closing bank...")
            pyautogui.press('esc')
            Movement.delay(0.6, 0.2)
            
            print("  ✅ Banking complete")
            return True
        
        return False
    
    def _make(self):
        """Make potions."""
        print("\n⚗️  [MAKING POTIONS]")
        
        for attempt in range(self.max_retries):
            slots = self.setup.positions['inventory_slots']
            
            # Herb (slot 0)
            print(f"  Clicking herb... (attempt {attempt + 1}/{self.max_retries})")
            x, y = slots[0]
            Movement.move_click(x, y)
            Movement.delay(0.4, 0.1)
            
            # Secondary (slot 14)
            print(f"  Clicking {self.setup.potion_data['secondary']}...")
            x, y = slots[14]
            Movement.move_click(x, y)
            Movement.delay(1.2, 0.3)
            
            # Space to confirm
            print("  Pressing Space...")
            pyautogui.press('space')
            Movement.delay(0.6, 0.2)
            
            # Wait for potions to finish
            wait = random.uniform(17, 21)
            print(f"  ⏳ Crafting potions ({wait:.1f}s)...")
            time.sleep(wait)
            
            print("  ✅ Potions complete")
            return True
        
        return False
    
    def _stats(self):
        """Print stats."""
        s = self.xp.stats()
        print(f"\n📊 Stats: {s['potions']:,} potions | {s['xp']:,.0f} XP | "
              f"{s['xp_hour']:,.0f}/hr | {s['potions_hour']:,.0f} p/hr | {s['runtime']}")


def main():
    """Main."""
    setup = Setup()
    
    if setup.load():
        print("\n" + "="*60)
        print("📁 EXISTING CONFIGURATION FOUND")
        print("="*60)
        if input("Reuse this setup? (y/n): ").strip().lower() != 'y':
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
