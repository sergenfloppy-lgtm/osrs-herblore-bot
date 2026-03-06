#!/usr/bin/env python3
"""OSRS Herblore Bot - Main Entry Point"""
import sys
import json
from src.utils.screen import find_game_region
from src.bot.herblore import HerbloreBot


def print_banner():
    """Print welcome banner."""
    print("""
╔═══════════════════════════════════════╗
║   OSRS Herblore Bot v1.0              ║
║   Educational purposes only           ║
║   Botting violates OSRS ToS           ║
╚═══════════════════════════════════════╝
    """)


def list_potions():
    """List available potions."""
    with open('data/potions.json', 'r') as f:
        data = json.load(f)
    
    print("\nAvailable Potions:")
    print("-" * 60)
    for i, potion in enumerate(data['potions'], 1):
        print(f"{i:2d}. {potion['name']:<20} (Lvl {potion['level']:2d}, {potion['xp']:5.1f} XP)")
        print(f"    Herb: {potion['herb']}, Secondary: {potion['secondary']}")
    print("-" * 60)


def setup_wizard():
    """Interactive setup wizard."""
    print_banner()
    
    print("\n[SETUP] Game Window Region")
    print("We need to define your OSRS game window region.")
    game_region = find_game_region()
    print(f"Game region set: {game_region}\n")
    
    # Select potion
    list_potions()
    
    while True:
        try:
            choice = input("\nSelect potion number (or name): ").strip()
            
            # Try as number first
            try:
                choice_num = int(choice)
                with open('data/potions.json', 'r') as f:
                    data = json.load(f)
                if 1 <= choice_num <= len(data['potions']):
                    potion_name = data['potions'][choice_num - 1]['name']
                    break
            except ValueError:
                # Try as name
                with open('data/potions.json', 'r') as f:
                    data = json.load(f)
                potions = [p['name'] for p in data['potions']]
                if choice in potions:
                    potion_name = choice
                    break
            
            print("Invalid selection. Try again.")
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(0)
    
    return game_region, potion_name


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_potions()
        sys.exit(0)
    
    # Run setup wizard
    game_region, potion_name = setup_wizard()
    
    print(f"\n[BOT] Starting bot for {potion_name}...")
    print("[BOT] Make sure:")
    print("  1. You are logged into OSRS")
    print("  2. You are standing next to a bank")
    print("  3. Bank contains herbs and vials of water")
    print("  4. Press Ctrl+C to stop anytime")
    
    input("\nPress Enter to start the bot...")
    
    try:
        bot = HerbloreBot(game_region, potion_name)
        bot.start()
    except Exception as e:
        print(f"\n[ERROR] Bot crashed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
