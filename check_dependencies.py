#!/usr/bin/env python3
"""Check if all dependencies are installed."""
import sys

def check_dependencies():
    """Check each required dependency."""
    missing = []
    
    dependencies = {
        'mss': 'Screen capture library',
        'cv2': 'OpenCV (opencv-python)',
        'numpy': 'NumPy arrays',
        'PIL': 'Pillow image library',
        'pyautogui': 'Mouse/keyboard control',
        'PyQt6': 'GUI framework (optional)',
        'scipy': 'Scientific computing',
    }
    
    print("Checking dependencies...")
    print("-" * 60)
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module:<15} - {description}")
        except ImportError:
            print(f"❌ {module:<15} - {description} - NOT INSTALLED")
            missing.append(module)
    
    print("-" * 60)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} dependencies!")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nOr install individually:")
        for module in missing:
            if module == 'cv2':
                print(f"  pip install opencv-python")
            elif module == 'PIL':
                print(f"  pip install pillow")
            else:
                print(f"  pip install {module}")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

if __name__ == '__main__':
    if not check_dependencies():
        sys.exit(1)
