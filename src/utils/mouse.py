"""Humanized mouse movement with anti-detection."""
import pyautogui
import random
import time
import numpy as np
from scipy.interpolate import interp1d

pyautogui.PAUSE = 0  # We handle delays ourselves


def gaussian_delay(mean=0.15, std=0.05):
    """Random delay with Gaussian distribution."""
    delay = max(0.05, random.gauss(mean, std))
    time.sleep(delay)


def bezier_curve(start, end, control_points=2):
    """Generate Bezier curve points between start and end."""
    if control_points == 0:
        return [start, end]
    
    # Generate random control points
    points = [start]
    for i in range(control_points):
        t = (i + 1) / (control_points + 1)
        x = start[0] + t * (end[0] - start[0]) + random.randint(-50, 50)
        y = start[1] + t * (end[1] - start[1]) + random.randint(-50, 50)
        points.append((x, y))
    points.append(end)
    
    # Create Bezier curve
    n = len(points)
    t_values = np.linspace(0, 1, 50)
    curve_x, curve_y = [], []
    
    for t in t_values:
        x = sum(
            points[i][0] * (1 - t) ** (n - 1 - i) * t ** i * np.math.comb(n - 1, i)
            for i in range(n)
        )
        y = sum(
            points[i][1] * (1 - t) ** (n - 1 - i) * t ** i * np.math.comb(n - 1, i)
            for i in range(n)
        )
        curve_x.append(x)
        curve_y.append(y)
    
    return list(zip(curve_x, curve_y))


def humanized_move(x, y, misclick_chance=0.05):
    """Move mouse to (x, y) with human-like behavior."""
    current = pyautogui.position()
    
    # Random chance to misclick slightly off-target first
    if random.random() < misclick_chance:
        offset_x = x + random.randint(-10, 10)
        offset_y = y + random.randint(-10, 10)
        path = bezier_curve(current, (offset_x, offset_y), control_points=1)
        for px, py in path[::2]:  # Skip some points for speed
            pyautogui.moveTo(int(px), int(py))
            time.sleep(0.001)
        gaussian_delay(0.05, 0.02)
    
    # Move to actual target
    path = bezier_curve(current if random.random() < misclick_chance else pyautogui.position(), (x, y), control_points=random.randint(1, 3))
    for px, py in path[::2]:
        pyautogui.moveTo(int(px), int(py))
        time.sleep(0.001)
    
    gaussian_delay()


def humanized_click(x=None, y=None, button='left', clicks=1):
    """Click with humanized timing."""
    if x is not None and y is not None:
        humanized_move(x, y)
    
    for _ in range(clicks):
        # Random pre-click delay
        time.sleep(random.uniform(0.01, 0.05))
        pyautogui.click(button=button)
        gaussian_delay(0.1, 0.03)


def random_mouse_movement():
    """Occasionally move mouse randomly (anti-bot)."""
    if random.random() < 0.1:  # 10% chance
        current = pyautogui.position()
        offset_x = current[0] + random.randint(-100, 100)
        offset_y = current[1] + random.randint(-100, 100)
        humanized_move(offset_x, offset_y)
