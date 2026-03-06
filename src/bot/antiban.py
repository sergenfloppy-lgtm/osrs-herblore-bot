"""Anti-detection and anti-ban features."""
import random
import time
from datetime import datetime, timedelta


class AntiBan:
    """Humanization and anti-detection features."""
    
    def __init__(self):
        self.last_break_time = datetime.now()
        self.session_start = datetime.now()
        self.total_actions = 0
        self.next_break = self._calculate_next_break()
        self.max_session_duration = random.randint(4, 6) * 3600  # 4-6 hours
    
    def _calculate_next_break(self):
        """Calculate next break time."""
        minutes = random.randint(15, 45)
        return datetime.now() + timedelta(minutes=minutes)
    
    def should_take_break(self):
        """Check if it's time for a break."""
        return datetime.now() >= self.next_break
    
    def take_break(self):
        """Take a randomized break."""
        duration = random.randint(60, 180)  # 1-3 minutes
        print(f"[ANTIBAN] Taking break for {duration} seconds...")
        time.sleep(duration)
        self.last_break_time = datetime.now()
        self.next_break = self._calculate_next_break()
    
    def should_end_session(self):
        """Check if session has been running too long."""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        return elapsed >= self.max_session_duration
    
    def random_camera_movement(self):
        """Randomly adjust camera angle."""
        if random.random() < 0.05:  # 5% chance
            # This would use keyboard arrow keys to rotate camera
            # Placeholder for now
            pass
    
    def random_skill_check(self):
        """Randomly open skills tab (looks human)."""
        if random.random() < 0.02:  # 2% chance
            # This would open skills interface
            # Placeholder for now
            pass
    
    def random_right_click(self):
        """Occasionally right-click randomly (looks exploratory)."""
        if random.random() < 0.03:  # 3% chance
            # Right-click somewhere random
            # Placeholder for now
            pass
    
    def action_delay(self, base=0.5, variance=0.2):
        """
        Delay between actions with variation.
        base: base delay in seconds
        variance: standard deviation
        """
        delay = max(0.1, random.gauss(base, variance))
        time.sleep(delay)
    
    def increment_action(self):
        """Track action count."""
        self.total_actions += 1
        
        # Every N actions, do something random
        if self.total_actions % 50 == 0:
            self.random_camera_movement()
        if self.total_actions % 100 == 0:
            self.random_skill_check()
    
    def get_session_stats(self):
        """Get session statistics."""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        return {
            'elapsed_seconds': int(elapsed),
            'elapsed_formatted': str(timedelta(seconds=int(elapsed))),
            'total_actions': self.total_actions,
            'actions_per_minute': self.total_actions / (elapsed / 60) if elapsed > 0 else 0,
            'next_break_in': (self.next_break - datetime.now()).total_seconds(),
            'session_limit': self.max_session_duration,
        }
