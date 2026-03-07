#!/usr/bin/env python3
"""
OSRS Herblore Bot - Production v4
- Dialogue box validation
- Visual overlay for click zones
- One-click recording mode
- Enhanced validation learning
"""
import time
import random
import json
import math
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import threading

print("""
╔═══════════════════════════════════════════════════════════╗
║   OSRS Herblore Bot v4                                    ║
║   Dialogue Validation | Visual Overlay | Smart Recording  ║
╚═══════════════════════════════════════════════════════════╝
""")

try:
    import pyautogui
    import mss
    import cv2
    from PIL import Image, ImageDraw, ImageFont
    from pynput import mouse, keyboard as pynput_keyboard
    print("✅ Ready\n")
except ImportError as e:
    print(f"❌ Missing: {e}")
    print("Install: pip install pyautogui mss opencv-python pillow pynput")
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


class VisualOverlay:
    """Visual overlay to show click variance zones."""
    
    def __init__(self):
        self.overlay_window = None
        self.zones = []
    
    def add_zone(self, x, y, variance=15, label=""):
        """Add a click zone to display."""
        self.zones.append({
            'x': x,
            'y': y,
            'variance': variance,
            'label': label
        })
    
    def show(self, duration=3):
        """Show overlay for specified duration."""
        print(f"📍 Showing overlay for {duration}s...")
        
        # Capture screen
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = np.array(sct.grab(monitor))
        
        # Convert to PIL
        img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Draw each zone
        for zone in self.zones:
            x, y = zone['x'], zone['y']
            var = zone['variance']
            label = zone['label']
            
            # Draw semi-transparent square
            left = x - var
            top = y - var
            right = x + var
            bottom = y + var
            
            # Yellow square with transparency
            draw.rectangle([left, top, right, bottom], 
                         outline=(255, 255, 0, 255), 
                         fill=(255, 255, 0, 50), 
                         width=2)
            
            # Draw crosshair at center
            draw.line([x - 5, y, x + 5, y], fill=(255, 0, 0, 255), width=2)
            draw.line([x, y - 5, x, y + 5], fill=(255, 0, 0, 255), width=2)
            
            # Label
            if label:
                try:
                    font = ImageFont.truetype("arial.ttf", 14)
                except:
                    font = ImageFont.load_default()
                draw.text((x + var + 5, y - var), label, fill=(255, 255, 0, 255), font=font)
        
        # Save temporarily
        img.save('overlay_preview.png')
        print(f"✅ Overlay saved to: overlay_preview.png")
        print(f"   Yellow squares show ±{self.zones[0]['variance']}px click zones")
        print(f"   Red crosshairs show center points")
        
        self.zones.clear()
    
    def clear(self):
        """Clear all zones."""
        self.zones.clear()


class RecordingSetup:
    """One-click recording mode for setup."""
    
    def __init__(self):
        self.positions = {}
        self.templates = {}
        self.potion_data = None
        self.recording = False
        self.current_step = None
        self.steps = []
        self.overlay = VisualOverlay()
    
    def on_click(self, x, y, button, pressed):
        """Handle mouse click during recording."""
        if not self.recording or not pressed:
            return
        
        if button == mouse.Button.left and self.current_step:
            # Capture this position
            print(f"  📍 Captured: {self.current_step['name']} at ({x}, {y})")
            
            # Screenshot around click (create new mss instance for thread safety)
            with mss.mss() as sct:
                region = {'left': x - 35, 'top': y - 35, 'width': 70, 'height': 70}
                screenshot = np.array(sct.grab(region))
                
                if screenshot.shape[2] == 4:
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                
                self.templates[self.current_step['name']] = screenshot
                self.positions[self.current_step['name']] = (x, y)
                
                # Save template
                Path('templates').mkdir(exist_ok=True)
                img = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
                img.save(f"templates/{self.current_step['name']}.png")
            
            # Move to next step (outside with block)
            self.current_step['captured'] = True
            self._advance_step()
    
    def on_key_press(self, key):
        """Handle keyboard press during recording."""
        if not self.recording:
            return
        
        try:
            # Record keyboard actions
            if hasattr(key, 'char') and key.char:
                print(f"  ⌨️  Recorded key: {key.char}")
            elif key == pynput_keyboard.Key.space:
                print(f"  ⌨️  Recorded key: SPACE")
            elif key == pynput_keyboard.Key.esc:
                print(f"  ⌨️  Recorded key: ESC")
        except:
            pass
    
    def _advance_step(self):
        """Move to next recording step."""
        # Find next uncaptured step
        for step in self.steps:
            if not step.get('captured', False):
                self.current_step = step
                print(f"\n{'='*60}")
                print(f"📍 NEXT: {step['name'].upper()}")
                print(f"{'='*60}")
                print(step['instruction'])
                return
        
        # All done
        self.recording = False
        self.current_step = None
        print("\n✅ Recording complete!")
    
    def run(self):
        """Run recording mode setup."""
        print("\n" + "="*60)
        print("🎬 RECORDING MODE SETUP")
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
        
        # Define recording steps
        self.steps = [
            {
                'name': 'bank',
                'instruction': '🏦 Click the bank booth/chest to record its position.',
                'captured': False
            },
            {
                'name': 'deposit',
                'instruction': '📤 Open the bank, then click "Deposit Inventory" button.',
                'captured': False
            },
            {
                'name': 'herb',
                'instruction': f"🌿 Click '{self.potion_data['herb']}' in your bank.",
                'captured': False
            },
            {
                'name': 'secondary',
                'instruction': f"🧪 Click '{self.potion_data['secondary']}' in your bank.",
                'captured': False
            },
            {
                'name': 'inv_first',
                'instruction': '📦 Close bank, then click the first inventory slot (top-left).',
                'captured': False
            },
            {
                'name': 'herb_inv',
                'instruction': f"🌿 [POTION MAKING] Withdraw 14 {self.potion_data['herb']} + 14 {self.potion_data['secondary']}, then click the HERB in your inventory (where it appears).",
                'captured': False
            },
            {
                'name': 'secondary_inv',
                'instruction': f"🧪 [POTION MAKING] Now click the {self.potion_data['secondary']} in your inventory (where it appears).",
                'captured': False
            },
        ]
        
        print("\n" + "="*60)
        print("🎬 STARTING RECORDING")
        print("="*60)
        print("⚠️  Just CLICK each item as you normally would.")
        print("⚠️  Bot will automatically capture each click.")
        print("⚠️  No need to press Enter between steps!")
        
        input("\n👉 Press Enter to start recording...")
        
        # Start recording
        self.recording = True
        self.current_step = self.steps[0]
        
        print(f"\n{'='*60}")
        print(f"📍 FIRST STEP: {self.current_step['name'].upper()}")
        print(f"{'='*60}")
        print(self.current_step['instruction'])
        
        # Start listeners
        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = pynput_keyboard.Listener(on_press=self.on_key_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # Wait for recording to complete
        while self.recording:
            time.sleep(0.1)
        
        mouse_listener.stop()
        keyboard_listener.stop()
        
        # Calculate inventory grid
        x, y = self.positions['inv_first']
        slots = [(x + col * 42, y + row * 36) for row in range(7) for col in range(4)]
        self.positions['inventory_slots'] = slots
        print(f"\n✅ Calculated {len(slots)} inventory slots")
        
        # Show overlay
        print("\n" + "="*60)
        print("📊 VISUAL OVERLAY")
        print("="*60)
        print("Showing click variance zones...")
        
        for name, value in self.positions.items():
            if name != 'inventory_slots':
                x, y = value
                self.overlay.add_zone(x, y, variance=15, label=name)
        
        self.overlay.show(duration=5)
        
        input("\n👉 Check overlay_preview.png, then press Enter...")
        
        # Save
        self._save()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print(f"📁 Configuration: bot_config.json")
        print(f"📁 Templates: templates/")
        print(f"📁 Overlay: overlay_preview.png")
        
        return True
    
    def _save(self):
        """Save configuration."""
        config = {
            'version': 4,
            'created': datetime.now().isoformat(),
            'potion': self.potion_data,
            'positions': self.positions,  # Save ALL positions including inventory_slots
            'variance': 15,
            'notes': {
                'herb': f"Shift+Click to withdraw {self.potion_data['herb']}",
                'secondary': f"Shift+Click to withdraw {self.potion_data['secondary']}",
                'herb_inv': f"Click {self.potion_data['herb']} in inventory",
                'secondary_inv': f"Click {self.potion_data['secondary']} in inventory",
                'inventory': "28 slots calculated (4 cols × 7 rows) + recorded herb/secondary positions",
                'variance': "±15 pixels per click"
            }
        }
        
        with open('bot_config.json', 'w') as f:
            json.dump(config, f, indent=2)


class Validator:
    """Enhanced validator with dialogue box checking."""
    
    def __init__(self, setup):
        self.setup = setup
        Path('validation_checks').mkdir(exist_ok=True)
        self.dialogue_template = None
    
    def check_clicked_correct_item(self, item_name, click_pos):
        """Verify we clicked the correct item."""
        print(f"  [VALIDATE] Checking {item_name}...")
        
        if item_name not in self.setup['templates']:
            print(f"  ⚠️  No template for {item_name}")
            return True
        
        # Capture area around click
        x, y = click_pos
        with mss.mss() as sct:
            region = {'left': x - 35, 'top': y - 35, 'width': 70, 'height': 70}
            screenshot = np.array(sct.grab(region))
        
        if screenshot.shape[2] == 4:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        # Compare with template
        template = self.setup['templates'][item_name]
        
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
        if screenshot.shape != template.shape:
            template = cv2.resize(template, (screenshot.shape[1], screenshot.shape[0]))
        
        # Calculate similarity
        gray_current = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(gray_current, gray_template)
        similarity = 1 - (np.sum(diff) / (gray_current.size * 255))
        
        # Save comparison
        self._save_comparison(item_name, screenshot, template, similarity)
        
        # Use variance to adjust threshold
        variance = self.setup['config'].get('variance', 15)
        # More variance = lower threshold (more lenient)
        threshold = 0.65 - (variance / 150)  # 15px variance = 0.55 threshold
        
        passed = similarity > threshold
        status = "✅" if passed else "❌"
        print(f"  {status} {item_name}: {similarity:.2f} (threshold: {threshold:.2f})")
        
        return passed
    
    def check_dialogue_appeared(self, dialogue_name="makex"):
        """Check if dialogue box appeared (e.g., Make-X interface)."""
        print(f"  [VALIDATE] Checking for {dialogue_name} dialogue...")
        
        # Capture center of screen (where dialogues appear)
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            center_x = monitor['width'] // 2
            center_y = monitor['height'] // 2
            
            # Capture 400x300 region in center
            region = {
                'left': center_x - 200,
                'top': center_y - 150,
                'width': 400,
                'height': 300
            }
            
            screenshot = np.array(sct.grab(region))
        
        if screenshot.shape[2] == 4:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        # Save for debugging
        Path('validation_checks').mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f'validation_checks/dialogue_{dialogue_name}_{timestamp}.png', screenshot)
        
        # Check for dialogue characteristics:
        # 1. Dark background (OSRS dialogues have dark backgrounds)
        # 2. Text present (lots of edges from text)
        
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Check average brightness (dialogues are darker)
        avg_brightness = np.mean(gray)
        is_dark = avg_brightness < 80  # Dark background
        
        # Check for text (high edge density)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges) / edges.size
        has_text = edge_density > 0.05  # Text creates edges
        
        # Check for UI elements (specific color ranges for OSRS UI)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        # OSRS UI brown color range
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([30, 255, 200])
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        has_ui = np.sum(brown_mask) > 1000  # UI elements present
        
        dialogue_present = (is_dark and has_text) or has_ui
        
        status = "✅" if dialogue_present else "❌"
        print(f"  {status} Dialogue check: dark={is_dark}, text={has_text}, ui={has_ui}")
        
        if not dialogue_present:
            print(f"  📸 Saved to: validation_checks/dialogue_{dialogue_name}_{timestamp}.png")
        
        return dialogue_present
    
    def _save_comparison(self, name, current, template, score):
        """Save visual comparison."""
        if current.shape[2] == 4:
            current = cv2.cvtColor(current, cv2.COLOR_BGRA2BGR)
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
        h, w = current.shape[:2]
        comparison = np.zeros((h, w * 2 + 10, 3), dtype=np.uint8)
        comparison[:, :w] = current
        comparison[:, w+10:] = template
        
        img = Image.fromarray(cv2.cvtColor(comparison, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        
        variance = self.setup['config'].get('variance', 15)
        threshold = 0.65 - (variance / 150)
        
        text = f"{name} | Score: {score:.2f} | Threshold: {threshold:.2f} | {'PASS' if score > threshold else 'FAIL'}"
        draw.text((10, 10), text, fill=(255, 255, 0))
        
        timestamp = datetime.now().strftime("%H%M%S")
        img.save(f'validation_checks/{name}_{timestamp}.png')


class Movement:
    """Enhanced movement with overlay support."""
    
    recent_positions = []
    max_history = 10
    
    @staticmethod
    def get_varied_position(base_x, base_y, variance=15):
        """Get varied position within variance zone."""
        attempts = 0
        max_attempts = 20
        
        while attempts < max_attempts:
            offset_x = random.randint(-variance, variance)
            offset_y = random.randint(-variance, variance)
            
            new_x = base_x + offset_x
            new_y = base_y + offset_y
            
            too_close = False
            for old_x, old_y in Movement.recent_positions:
                distance = math.sqrt((new_x - old_x)**2 + (new_y - old_y)**2)
                if distance < 8:
                    too_close = True
                    break
            
            if not too_close:
                Movement.recent_positions.append((new_x, new_y))
                if len(Movement.recent_positions) > Movement.max_history:
                    Movement.recent_positions.pop(0)
                return (new_x, new_y)
            
            attempts += 1
        
        return (base_x + offset_x, base_y + offset_y)
    
    @staticmethod
    def move_click(x, y, offset=15):
        """Smooth movement with variance."""
        start = pyautogui.position()
        x, y = Movement.get_varied_position(x, y, offset)
        
        distance = math.sqrt((x - start[0])**2 + (y - start[1])**2)
        num_points = random.randint(25, 35) + int(distance / 20)
        
        ctrl1_x = start[0] + (x - start[0]) * random.uniform(0.20, 0.35) + random.randint(-60, 60)
        ctrl1_y = start[1] + (y - start[1]) * random.uniform(0.20, 0.35) + random.randint(-60, 60)
        ctrl2_x = start[0] + (x - start[0]) * random.uniform(0.65, 0.80) + random.randint(-60, 60)
        ctrl2_y = start[1] + (y - start[1]) * random.uniform(0.65, 0.80) + random.randint(-60, 60)
        
        if random.random() < 0.3:
            ctrl1_x += random.randint(-30, 30)
            ctrl2_y += random.randint(-30, 30)
        
        for i in range(num_points + 1):
            t = i / num_points
            
            if t < 0.05:
                t_eased = t * t * 0.5
            elif t < 0.92:
                t_eased = t * t * (3 - 2 * t)
            else:
                overshoot = (t - 0.92) * 2
                t_eased = 0.92 + overshoot * (1.1 if random.random() < 0.5 else 1.05)
            
            t_eased = max(0, min(1, t_eased))
            
            px = ((1-t_eased)**3 * start[0] + 3*(1-t_eased)**2*t_eased * ctrl1_x + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_x + t_eased**3 * x)
            py = ((1-t_eased)**3 * start[1] + 3*(1-t_eased)**2*t_eased * ctrl1_y + 
                  3*(1-t_eased)*t_eased**2 * ctrl2_y + t_eased**3 * y)
            
            if random.random() < 0.15 and i > 5:
                px += random.uniform(-0.5, 0.5)
                py += random.uniform(-0.5, 0.5)
            
            pyautogui.moveTo(int(px), int(py))
            
            if i < 5 or i > num_points - 5:
                delay = random.uniform(0.005, 0.012)
            elif random.random() < 0.1:
                delay = random.uniform(0.008, 0.015)
            else:
                delay = random.uniform(0.001, 0.004)
            
            time.sleep(delay)
        
        time.sleep(random.uniform(0.08, 0.18))
        
        if random.random() < 0.40:
            adjust_x = random.randint(-2, 2)
            adjust_y = random.randint(-2, 2)
            pyautogui.moveRel(adjust_x, adjust_y)
            time.sleep(random.uniform(0.02, 0.05))
        
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.025, 0.095))
        pyautogui.mouseUp()
        
        if random.random() < 0.20:
            time.sleep(random.uniform(0.01, 0.03))
            pyautogui.moveRel(random.randint(-3, 3), random.randint(-3, 3))
    
    @staticmethod
    def delay(base, variation=0.3):
        """Gaussian delay."""
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
    """Main bot with dialogue validation."""
    
    def __init__(self, setup_data):
        self.setup = setup_data
        self.validator = Validator(setup_data)
        self.xp = XPTracker(setup_data['config']['potion']['xp'])
        self.running = True
        self.max_retries = 3
    
    def start(self):
        """Start bot."""
        potion = self.setup['config']['potion']
        
        print("\n" + "="*60)
        print(f"🤖 BOT STARTING")
        print("="*60)
        print(f"🎯 Potion: {potion['name']}")
        print(f"🌿 Herb: {potion['herb']}")
        print(f"🧪 Secondary: {potion['secondary']}")
        print(f"📊 XP: {potion['xp']} per potion")
        print(f"📍 Variance: ±{self.setup['config']['variance']}px")
        print("="*60)
        print("\n⚠️  Dialogue validation enabled")
        print("⚠️  Check validation_checks/ for images")
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
                    print("❌ Banking failed after retries")
                    break
                
                if not self._make():
                    print("❌ Making failed after retries")
                    break
                
                self.xp.add(14)
                self._stats()
                
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
            x, y = self.setup['positions']['bank']
            Movement.move_click(x, y)
            Movement.delay(2.0, 0.4)
            
            if not self.validator.check_clicked_correct_item('bank', (x, y)):
                print("  ⚠️  Bank misclick - retrying...")
                continue
            
            # Deposit
            print("  Depositing inventory...")
            x, y = self.setup['positions']['deposit']
            Movement.move_click(x, y)
            Movement.delay(0.8, 0.2)
            
            # Withdraw herbs
            print(f"  Withdrawing {self.setup['config']['potion']['herb']}...")
            x, y = self.setup['positions']['herb']
            
            pyautogui.keyDown('shift')
            Movement.move_click(x, y)
            pyautogui.keyUp('shift')
            Movement.delay(0.8, 0.2)
            
            if not self.validator.check_clicked_correct_item('herb', (x, y)):
                print("  ⚠️  Herb misclick - retrying...")
                pyautogui.press('esc')
                continue
            
            # Withdraw secondary
            print(f"  Withdrawing {self.setup['config']['potion']['secondary']}...")
            x, y = self.setup['positions']['secondary']
            
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
        """Make potions with dialogue validation."""
        print("\n⚗️  [MAKING POTIONS]")
        print("   📝 Step 1: Click herb in inventory")
        print("   📝 Step 2: Click secondary in inventory")
        print("   📝 Step 3: Wait for Make-X dialogue")
        print("   📝 Step 4: Press Space to confirm")
        print("   📝 Step 5: Wait for potions to finish")
        
        for attempt in range(self.max_retries):
            # Use recorded positions for herb and secondary in inventory
            herb_pos = self.setup['positions'].get('herb_inv')
            secondary_pos = self.setup['positions'].get('secondary_inv')
            
            if not herb_pos or not secondary_pos:
                print("  ⚠️  Missing recorded positions for inventory items!")
                print("  ⚠️  Please run setup again and record herb_inv + secondary_inv")
                return False
            
            # Herb in inventory
            print(f"\n  Step 1: Clicking {self.setup['config']['potion']['herb']} in inventory... (attempt {attempt + 1}/{self.max_retries})")
            x, y = herb_pos
            Movement.move_click(x, y)
            Movement.delay(0.4, 0.1)
            
            # Secondary in inventory
            print(f"  Step 2: Clicking {self.setup['config']['potion']['secondary']} in inventory...")
            x, y = secondary_pos
            Movement.move_click(x, y)
            Movement.delay(1.5, 0.3)  # Wait longer for dialogue
            
            # CHECK FOR DIALOGUE
            print(f"  Step 3: Checking for Make-X dialogue...")
            if not self.validator.check_dialogue_appeared("makex"):
                print("  ⚠️  Make-X dialogue didn't appear - retrying...")
                pyautogui.press('esc')  # Close any open interfaces
                Movement.delay(0.5, 0.1)
                continue
            
            # Space to confirm
            print("  Step 4: Pressing Space to confirm...")
            pyautogui.press('space')
            Movement.delay(0.6, 0.2)
            
            # Wait for potions
            wait = random.uniform(17, 21)
            print(f"  Step 5: ⏳ Crafting potions ({wait:.1f}s)...")
            time.sleep(wait)
            
            print("  ✅ Potions complete")
            return True
        
        return False
    
    def _stats(self):
        """Print stats."""
        s = self.xp.stats()
        print(f"\n📊 Stats: {s['potions']:,} potions | {s['xp']:,.0f} XP | "
              f"{s['xp_hour']:,.0f}/hr | {s['potions_hour']:,.0f} p/hr | {s['runtime']}")


def load_setup():
    """Load existing setup."""
    if not Path('bot_config.json').exists():
        return None
    
    try:
        with open('bot_config.json', 'r') as f:
            config = json.load(f)
        
        # Load templates
        templates = {}
        for file in Path('templates').glob('*.png'):
            name = file.stem
            img = cv2.imread(str(file))
            if img is not None:
                templates[name] = img
        
        return {
            'config': config,
            'positions': config['positions'],
            'templates': templates
        }
    except Exception as e:
        print(f"⚠️  Load failed: {e}")
        return None


def main():
    """Main."""
    setup_data = load_setup()
    
    if setup_data:
        print("\n" + "="*60)
        print("📁 EXISTING CONFIGURATION FOUND")
        print("="*60)
        potion = setup_data['config']['potion']
        print(f"🎯 Potion: {potion['name']}")
        print(f"🌿 Herb: {potion['herb']}")
        print(f"🧪 Secondary: {potion['secondary']}")
        print(f"📅 Created: {setup_data['config'].get('created', 'Unknown')}")
        
        if input("\nReuse this setup? (y/n): ").strip().lower() != 'y':
            recorder = RecordingSetup()
            recorder.run()
            setup_data = load_setup()
    else:
        recorder = RecordingSetup()
        recorder.run()
        setup_data = load_setup()
    
    if setup_data:
        bot = Bot(setup_data)
        bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter...")
