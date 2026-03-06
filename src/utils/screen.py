"""Screen capture and utilities."""
import mss
import numpy as np
from PIL import Image
import pyautogui


class ScreenCapture:
    """Fast screen capture using mss."""
    
    def __init__(self):
        self.sct = mss.mss()
    
    def capture(self, region=None):
        """
        Capture screen region.
        region: (x, y, width, height) or None for full screen
        Returns: PIL Image
        """
        if region is None:
            monitor = self.sct.monitors[1]  # Primary monitor
        else:
            x, y, w, h = region
            monitor = {"top": y, "left": x, "width": w, "height": h}
        
        screenshot = self.sct.grab(monitor)
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    def capture_array(self, region=None):
        """Capture as numpy array (for OpenCV)."""
        img = self.capture(region)
        return np.array(img)
    
    def get_game_window(self):
        """
        Attempt to find OSRS game window.
        Returns: (x, y, width, height) or None
        """
        # This would need platform-specific window detection
        # For now, return None (use full screen or user-defined region)
        return None


def find_game_region():
    """
    Helper to let user define game region.
    Returns: (x, y, width, height)
    """
    print("Move mouse to TOP-LEFT corner of game window and press Enter...")
    input()
    top_left = pyautogui.position()
    
    print("Move mouse to BOTTOM-RIGHT corner of game window and press Enter...")
    input()
    bottom_right = pyautogui.position()
    
    x, y = top_left
    width = bottom_right[0] - x
    height = bottom_right[1] - y
    
    return (x, y, width, height)
