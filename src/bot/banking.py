"""Banking logic."""
import time
from src.utils.mouse import humanized_click, gaussian_delay
from src.bot.detection import Detector


class Banking:
    """Handle bank interactions."""
    
    def __init__(self, detector: Detector, game_region):
        self.detector = detector
        self.game_region = game_region
        self.bank_open = False
    
    def open_bank(self, screen_capture):
        """
        Open bank (assumes player is near banker/chest).
        Returns: bool (success)
        """
        if self.bank_open:
            return True
        
        # Get screenshot
        screenshot = screen_capture.capture_array(self.game_region)
        
        # Check if already open
        if self.detector.detect_bank_interface(screenshot):
            self.bank_open = True
            return True
        
        # Click banker (this would need actual position detection)
        # For now, assume a known position or template matching
        # Placeholder: click center of screen
        center_x = self.game_region[0] + self.game_region[2] // 2
        center_y = self.game_region[1] + self.game_region[3] // 2
        
        humanized_click(center_x, center_y)
        gaussian_delay(0.5, 0.1)
        
        # Wait for interface to open
        time.sleep(1)
        screenshot = screen_capture.capture_array(self.game_region)
        self.bank_open = self.detector.detect_bank_interface(screenshot)
        
        return self.bank_open
    
    def close_bank(self):
        """Close bank interface."""
        if not self.bank_open:
            return True
        
        # Press ESC key to close
        import pyautogui
        pyautogui.press('esc')
        gaussian_delay(0.3, 0.1)
        self.bank_open = False
        return True
    
    def withdraw_item(self, item_name, quantity='all'):
        """
        Withdraw item from bank.
        quantity: 'all', number, or 'x'
        Returns: bool (success)
        """
        if not self.bank_open:
            return False
        
        # This would use template matching to find item in bank
        # then right-click and select withdraw option
        # Placeholder implementation
        
        # Assume item is at a known slot (would need detection)
        # Click item slot
        bank_x = self.game_region[0] + 100
        bank_y = self.game_region[1] + 100
        
        if quantity == 'all':
            # Left-click for withdraw-all (if set as default)
            humanized_click(bank_x, bank_y)
        else:
            # Right-click for menu
            humanized_click(bank_x, bank_y, button='right')
            gaussian_delay(0.2, 0.05)
            # Click withdraw option (would need menu detection)
            humanized_click(bank_x, bank_y + 40)
        
        gaussian_delay(0.3, 0.1)
        return True
    
    def deposit_all(self):
        """Deposit all items in inventory."""
        if not self.bank_open:
            return False
        
        # Click "Deposit Inventory" button
        # Button is typically bottom-right of bank interface
        deposit_x = self.game_region[0] + self.game_region[2] - 100
        deposit_y = self.game_region[1] + self.game_region[3] - 100
        
        humanized_click(deposit_x, deposit_y)
        gaussian_delay(0.4, 0.1)
        return True
    
    def deposit_item(self, slot_number):
        """
        Deposit specific inventory slot.
        slot_number: 0-27
        """
        if not self.bank_open:
            return False
        
        # Get inventory slot position
        slots = self.detector.detect_inventory_slots(None)
        if slot_number >= len(slots):
            return False
        
        x, y = slots[slot_number]
        humanized_click(
            self.game_region[0] + x,
            self.game_region[1] + y
        )
        gaussian_delay(0.2, 0.05)
        return True
    
    def has_items(self, screen_capture):
        """Check if inventory has items."""
        screenshot = screen_capture.capture_array(self.game_region)
        count = self.detector.count_items_in_inventory(screenshot)
        return count > 0
