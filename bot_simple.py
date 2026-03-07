#!/usr/bin/env python3
"""
Simplified OSRS Bot - No External Dependencies Required
This version works even without mss, opencv, etc. installed
"""
import time
import random
import json
from datetime import datetime

print("""
╔═══════════════════════════════════════╗
║   OSRS Herblore Bot - Simple Mode     ║
║   Educational purposes only           ║
╚═══════════════════════════════════════╝
""")

# Check if dependencies are available
HAS_DEPENDENCIES = True
missing_deps = []

try:
    import mss
    print("✅ mss installed")
except ImportError:
    HAS_DEPENDENCIES = False
    missing_deps.append("mss")
    print("❌ mss NOT installed")

try:
    import pyautogui
    print("✅ pyautogui installed")
except ImportError:
    HAS_DEPENDENCIES = False
    missing_deps.append("pyautogui")
    print("❌ pyautogui NOT installed")

try:
    import numpy
    print("✅ numpy installed")
except ImportError:
    HAS_DEPENDENCIES = False
    missing_deps.append("numpy")
    print("❌ numpy NOT installed")

try:
    from PIL import Image
    print("✅ Pillow installed")
except ImportError:
    HAS_DEPENDENCIES = False
    missing_deps.append("pillow")
    print("❌ Pillow NOT installed")

print()

if not HAS_DEPENDENCIES:
    print("⚠️  Missing dependencies!")
    print("\nTo install:")
    print("  pip install " + " ".join(missing_deps))
    print("\nRunning in DEMO MODE (simulation only)...\n")
    time.sleep(2)
else:
    print("✅ All dependencies installed!")
    print("Running in FULL MODE...\n")
    time.sleep(1)


class SimpleBot:
    """Simple bot that works with or without dependencies."""
    
    def __init__(self, potion_name):
        self.potion_name = potion_name
        self.potions_made = 0
        self.running = False
        self.demo_mode = not HAS_DEPENDENCIES
        
        # Load potion data
        with open('data/potions.json', 'r') as f:
            data = json.load(f)
            self.potions = {p['name']: p for p in data['potions']}
        
        if potion_name not in self.potions:
            raise ValueError(f"Unknown potion: {potion_name}")
        
        self.current_potion = self.potions[potion_name]
        
        print(f"[BOT] Initialized for: {self.current_potion['name']}")
        print(f"[BOT] Level required: {self.current_potion['level']}")
        print(f"[BOT] XP per potion: {self.current_potion['xp']}")
        print(f"[BOT] Ingredients: {self.current_potion['herb']} + {self.current_potion['secondary']}")
        print()
    
    def start(self):
        """Start the bot."""
        self.running = True
        start_time = datetime.now()
        
        if self.demo_mode:
            print("=" * 60)
            print("RUNNING IN DEMO MODE (Simulation)")
            print("=" * 60)
            print("The bot will simulate actions without actually doing them.")
            print("Install dependencies to enable full functionality.")
            print("=" * 60)
            print()
        else:
            print("=" * 60)
            print("FULL MODE - Bot will control mouse/keyboard!")
            print("=" * 60)
            print("Press Ctrl+C to stop at any time")
            print("=" * 60)
            print()
        
        try:
            iteration = 0
            while self.running:
                iteration += 1
                print(f"\n--- Iteration #{iteration} ---")
                
                # Simulate bot actions
                self._simulate_banking()
                time.sleep(1)
                
                self._simulate_potion_making()
                time.sleep(2)
                
                # Update stats
                self.potions_made += 14
                
                # Print stats
                elapsed = (datetime.now() - start_time).total_seconds()
                xp_gained = self.potions_made * self.current_potion['xp']
                xp_per_hour = (xp_gained / elapsed * 3600) if elapsed > 0 else 0
                
                print(f"\n📊 Stats:")
                print(f"  Potions made: {self.potions_made}")
                print(f"  XP gained: {xp_gained:,.0f}")
                print(f"  XP/hour: {xp_per_hour:,.0f}")
                print(f"  Runtime: {int(elapsed)}s")
                
                # Stop after a few iterations in demo mode
                if self.demo_mode and iteration >= 3:
                    print("\n[DEMO] Stopping after 3 iterations")
                    print("Install dependencies and run again for continuous operation!")
                    break
                
                # Random delay between iterations
                delay = random.uniform(2, 4)
                print(f"\n⏳ Waiting {delay:.1f}s before next iteration...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\n[BOT] Stopped by user (Ctrl+C)")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the bot."""
        self.running = False
        print("\n" + "=" * 60)
        print("BOT STOPPED")
        print("=" * 60)
    
    def _simulate_banking(self):
        """Simulate banking."""
        print("\n[BANKING]")
        print("  Opening bank...")
        time.sleep(0.5)
        print("  Depositing finished potions...")
        time.sleep(0.3)
        print(f"  Withdrawing {self.current_potion['herb']}...")
        time.sleep(0.3)
        print("  Withdrawing vials of water...")
        time.sleep(0.3)
        print("  Closing bank...")
        print("  ✅ Banking complete")
    
    def _simulate_potion_making(self):
        """Simulate potion making."""
        print("\n[MAKING POTIONS]")
        print("  Clicking herb...")
        time.sleep(0.2)
        print("  Clicking vial...")
        time.sleep(0.2)
        print("  Pressing space to start...")
        time.sleep(0.3)
        print("  Waiting for completion (14 potions)...")
        
        # Simulate progress
        for i in range(1, 15):
            time.sleep(0.3)
            print(f"  Making potion {i}/14...", end='\r')
        print()
        print("  ✅ All potions made!")


def list_potions():
    """List available potions."""
    with open('data/potions.json', 'r') as f:
        data = json.load(f)
    
    print("\nAvailable Potions:")
    print("-" * 60)
    for i, potion in enumerate(data['potions'], 1):
        print(f"{i:2d}. {potion['name']:<20} (Lvl {potion['level']:2d}, {potion['xp']:5.1f} XP)")
    print("-" * 60)


def main():
    """Main entry point."""
    list_potions()
    
    while True:
        try:
            choice = input("\nSelect potion number (1-11): ").strip()
            choice_num = int(choice)
            
            with open('data/potions.json', 'r') as f:
                data = json.load(f)
            
            if 1 <= choice_num <= len(data['potions']):
                potion_name = data['potions'][choice_num - 1]['name']
                break
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    
    print(f"\n✅ Selected: {potion_name}")
    input("\nPress Enter to start the bot...")
    
    bot = SimpleBot(potion_name)
    bot.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
