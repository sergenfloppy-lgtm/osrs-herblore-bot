"""Computer vision and detection."""
import cv2
import numpy as np
from PIL import Image
import pytesseract


class Detector:
    """Detect game elements using CV."""
    
    def __init__(self, game_region):
        self.game_region = game_region
        self.templates = {}
    
    def load_template(self, name, path):
        """Load template image for matching."""
        self.templates[name] = cv2.imread(path, cv2.IMREAD_COLOR)
    
    def find_template(self, screenshot, template_name, threshold=0.8):
        """
        Find template in screenshot.
        Returns: (x, y, confidence) or None
        """
        if template_name not in self.templates:
            return None
        
        template = self.templates[template_name]
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            return (max_loc[0], max_loc[1], max_val)
        return None
    
    def detect_bank_interface(self, screenshot):
        """
        Detect if bank interface is open.
        Returns: bool
        """
        # Look for common bank colors (brown/tan UI)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
        
        # Brown/tan color range for OSRS bank interface
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([30, 255, 200])
        
        mask = cv2.inRange(hsv, lower_brown, upper_brown)
        bank_pixels = cv2.countNonZero(mask)
        
        # If significant brown pixels in center of screen, bank is likely open
        total_pixels = screenshot.shape[0] * screenshot.shape[1]
        return (bank_pixels / total_pixels) > 0.15
    
    def detect_inventory_slots(self, screenshot):
        """
        Detect inventory item slots.
        Returns: list of (x, y) coordinates
        """
        # OSRS inventory is a 4x7 grid typically in bottom-right
        # This is a simplified version - would need actual template matching
        slots = []
        
        # Approximate inventory region (right side, bottom portion)
        inv_x_start = int(self.game_region[2] * 0.7)
        inv_y_start = int(self.game_region[3] * 0.55)
        
        slot_width = 42
        slot_height = 36
        
        for row in range(7):
            for col in range(4):
                x = inv_x_start + col * slot_width
                y = inv_y_start + row * slot_height
                slots.append((x, y))
        
        return slots
    
    def count_items_in_inventory(self, screenshot, item_name=None):
        """
        Count items in inventory.
        Returns: int (total items or specific item count)
        """
        # This would use template matching or color detection
        # Simplified: count non-empty slots
        slots = self.detect_inventory_slots(screenshot)
        count = 0
        
        for x, y in slots:
            # Sample pixel at slot center
            if x < screenshot.shape[1] and y < screenshot.shape[0]:
                pixel = screenshot[y, x]
                # If pixel is not black/empty (simplified check)
                if np.sum(pixel) > 30:
                    count += 1
        
        return count
    
    def detect_make_x_interface(self, screenshot):
        """
        Detect "Make X" interface.
        Returns: bool
        """
        # Look for the interface prompt
        # Simplified: check for specific color patterns in center
        h, w = screenshot.shape[:2]
        center_region = screenshot[h//3:2*h//3, w//3:2*w//3]
        
        # Make-X interface has distinctive brown box
        hsv = cv2.cvtColor(center_region, cv2.COLOR_RGB2HSV)
        lower = np.array([10, 50, 50])
        upper = np.array([30, 255, 200])
        mask = cv2.inRange(hsv, lower, upper)
        
        return cv2.countNonZero(mask) > 1000
    
    def detect_player_nearby(self, screenshot):
        """
        Detect if another player is nearby.
        Returns: bool
        """
        # Look for yellow dots on minimap (other players)
        # This is simplified - would need actual minimap region + color detection
        # For now, return False
        return False
    
    def read_text(self, screenshot, region):
        """
        OCR text from region.
        region: (x, y, width, height) within screenshot
        Returns: str
        """
        x, y, w, h = region
        roi = screenshot[y:y+h, x:x+w]
        
        # Convert to PIL for pytesseract
        pil_img = Image.fromarray(roi)
        text = pytesseract.image_to_string(pil_img, config='--psm 7')
        return text.strip()
