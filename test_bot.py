#!/usr/bin/env python3
"""Test the bot in demo mode without actually clicking anything."""
import sys
sys.path.insert(0, '.')

from src.utils.logger import log_info, log_debug, log_error
from src.utils.screen import ScreenCapture
import time

def test_screen_capture():
    """Test screen capture functionality."""
    log_info("Testing screen capture...")
    
    # Define a test region (adjust these values)
    test_region = (100, 100, 800, 600)  # x, y, width, height
    
    log_info(f"Test region: {test_region}")
    
    try:
        capture = ScreenCapture()
        log_info("ScreenCapture object created")
        
        # Try to capture
        log_info("Attempting to capture screen...")
        img = capture.capture(test_region)
        
        if img:
            log_info(f"✅ Screen capture successful! Image size: {img.size}")
            
            # Try array capture
            log_info("Attempting array capture...")
            arr = capture.capture_array(test_region)
            if arr is not None:
                log_info(f"✅ Array capture successful! Shape: {arr.shape}")
            else:
                log_error("❌ Array capture returned None")
        else:
            log_error("❌ Screen capture returned None")
            
    except Exception as e:
        log_error(f"❌ Screen capture failed: {e}", exc_info=True)

def main():
    log_info("=" * 60)
    log_info("OSRS Bot Test Suite")
    log_info("=" * 60)
    
    test_screen_capture()
    
    log_info("=" * 60)
    log_info("Test complete. Check logs/bot_*.log for details")
    log_info("=" * 60)

if __name__ == '__main__':
    main()
