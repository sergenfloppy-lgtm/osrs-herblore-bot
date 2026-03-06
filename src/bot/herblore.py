"""Main Herblore training bot."""
import json
import time
from datetime import datetime
from src.utils.screen import ScreenCapture
from src.utils.mouse import humanized_click, gaussian_delay
from src.bot.detection import Detector
from src.bot.banking import Banking
from src.bot.antiban import AntiBan
from src.utils.logger import log_info, log_debug, log_error, log_warning


class HerbloreBot:
    """Main bot controller."""
    
    def __init__(self, game_region, potion_name):
        log_info(f"Initializing bot with game region: {game_region}")
        log_info(f"Selected potion: {potion_name}")
        
        self.game_region = game_region
        self.screen_capture = ScreenCapture()
        self.detector = Detector(game_region)
        self.banking = Banking(self.detector, game_region)
        self.antiban = AntiBan()
        
        # Load potion data
        log_debug("Loading potion data from data/potions.json")
        with open('data/potions.json', 'r') as f:
            data = json.load(f)
            self.potions = {p['name']: p for p in data['potions']}
        
        if potion_name not in self.potions:
            log_error(f"Unknown potion: {potion_name}")
            raise ValueError(f"Unknown potion: {potion_name}")
        
        self.current_potion = self.potions[potion_name]
        self.running = False
        
        # Statistics
        self.potions_made = 0
        self.xp_gained = 0
        self.start_time = None
        
        log_info("Bot initialized successfully")
    
    def start(self):
        """Start the bot."""
        self.running = True
        self.start_time = datetime.now()
        log_info(f"Starting Herblore bot for {self.current_potion['name']}")
        log_info(f"Required: {self.current_potion['herb']} + {self.current_potion['secondary']}")
        log_info("Bot loop starting...")
        
        try:
            iteration = 0
            while self.running:
                iteration += 1
                log_debug(f"Starting iteration #{iteration}")
                self._main_loop()
                log_debug(f"Completed iteration #{iteration}")
        except KeyboardInterrupt:
            log_info("Bot stopped by user (Ctrl+C)")
        except Exception as e:
            log_error(f"Bot crashed with exception: {e}", exc_info=True)
            raise
        finally:
            self.stop()
    
    def stop(self):
        """Stop the bot."""
        self.running = False
        self._print_stats()
    
    def _main_loop(self):
        """Main bot loop."""
        log_debug("Checking anti-ban conditions...")
        
        # Check anti-ban conditions
        if self.antiban.should_take_break():
            log_info("Taking scheduled break...")
            self.antiban.take_break()
        
        if self.antiban.should_end_session():
            log_info("Session time limit reached. Stopping...")
            self.running = False
            return
        
        # State machine
        log_debug(f"Capturing screen region: {self.game_region}")
        try:
            screenshot = self.screen_capture.capture_array(self.game_region)
            log_debug(f"Screenshot captured: {screenshot.shape if screenshot is not None else 'None'}")
        except Exception as e:
            log_error(f"Failed to capture screenshot: {e}", exc_info=True)
            time.sleep(1)
            return
        
        # 1. Check if inventory is empty -> go to bank
        log_debug("Checking if inventory has items...")
        has_items = self.banking.has_items(self.screen_capture)
        log_debug(f"Has items in inventory: {has_items}")
        
        if not has_items:
            log_info("Inventory empty - going to bank")
            self._bank_and_withdraw()
        else:
            log_info("Inventory has items - making potions")
            self._make_potions()
        
        self.antiban.increment_action()
        log_debug("Action incremented, loop iteration complete")
    
    def _bank_and_withdraw(self):
        """Bank finished potions and withdraw ingredients."""
        log_info("Banking...")
        
        # Open bank
        log_debug("Attempting to open bank...")
        if not self.banking.open_bank(self.screen_capture):
            log_error("Failed to open bank")
            gaussian_delay(2, 0.5)
            return
        
        log_info("Bank opened successfully")
        
        # Deposit all
        log_debug("Depositing all items...")
        self.banking.deposit_all()
        gaussian_delay(0.5, 0.1)
        
        # Withdraw grimy herbs (or clean herbs)
        log_info(f"Withdrawing {self.current_potion['herb']}...")
        self.banking.withdraw_item(self.current_potion['herb'], quantity='all')
        gaussian_delay(0.3, 0.1)
        
        # Withdraw vials of water (for unfinished potions)
        log_info("Withdrawing vials of water...")
        self.banking.withdraw_item('Vial of water', quantity='all')
        gaussian_delay(0.3, 0.1)
        
        # Close bank
        log_debug("Closing bank...")
        self.banking.close_bank()
        gaussian_delay(0.5, 0.1)
        log_info("Banking complete")
    
    def _make_potions(self):
        """Make potions from inventory items."""
        log_info("Making potions...")
        
        # Get inventory slots
        log_debug("Detecting inventory slots...")
        slots = self.detector.detect_inventory_slots(None)
        log_debug(f"Detected {len(slots)} inventory slots")
        
        # Click herb (first item)
        herb_x = self.game_region[0] + slots[0][0]
        herb_y = self.game_region[1] + slots[0][1]
        log_debug(f"Clicking herb at ({herb_x}, {herb_y})")
        humanized_click(herb_x, herb_y)
        gaussian_delay(0.2, 0.05)
        
        # Click vial of water (second item or known position)
        vial_x = self.game_region[0] + slots[14][0]  # Typically herbs fill first 14 slots
        vial_y = self.game_region[1] + slots[14][1]
        log_debug(f"Clicking vial at ({vial_x}, {vial_y})")
        humanized_click(vial_x, vial_y)
        gaussian_delay(0.3, 0.1)
        
        # Wait for "Make X" interface
        log_debug("Waiting for Make-X interface...")
        time.sleep(0.5)
        screenshot = self.screen_capture.capture_array(self.game_region)
        
        if self.detector.detect_make_x_interface(screenshot):
            log_info("Make-X interface detected")
            # Press spacebar or click to start making
            import pyautogui
            log_debug("Pressing spacebar to start making...")
            pyautogui.press('space')
            
            # Wait for completion (animation time)
            # Each potion takes ~2-3 seconds
            wait_time = 14 * 2.5  # 14 potions * 2.5 seconds each
            log_info(f"Waiting {wait_time}s for completion...")
            time.sleep(wait_time)
            
            # Update stats
            potions_this_batch = 14  # Assuming 14 herbs + 14 vials
            self.potions_made += potions_this_batch
            self.xp_gained += potions_this_batch * self.current_potion['xp']
            
            log_info(f"Batch complete: {potions_this_batch} potions made")
            self._print_stats()
        else:
            log_warning("Make-X interface not detected - might not have items or wrong screen")
            gaussian_delay(1, 0.2)
    
    def _print_stats(self):
        """Print current statistics."""
        if self.start_time is None:
            return
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        xp_per_hour = (self.xp_gained / elapsed * 3600) if elapsed > 0 else 0
        potions_per_hour = (self.potions_made / elapsed * 3600) if elapsed > 0 else 0
        
        print("\n" + "="*50)
        print(f"[STATS] Runtime: {int(elapsed // 60)}m {int(elapsed % 60)}s")
        print(f"[STATS] Potions made: {self.potions_made}")
        print(f"[STATS] XP gained: {self.xp_gained:,.0f}")
        print(f"[STATS] XP/hr: {xp_per_hour:,.0f}")
        print(f"[STATS] Potions/hr: {potions_per_hour:.1f}")
        
        # Antiban stats
        ab_stats = self.antiban.get_session_stats()
        print(f"[ANTIBAN] Actions: {ab_stats['total_actions']}")
        print(f"[ANTIBAN] Next break: {int(ab_stats['next_break_in'])}s")
        print("="*50 + "\n")
