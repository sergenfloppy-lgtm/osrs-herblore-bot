"""Configuration settings."""

# Default game region (x, y, width, height)
# User should set this to their OSRS game window
GAME_REGION = None  # Will be set during setup

# Anti-ban settings
BREAK_FREQUENCY_MIN = 15  # minutes
BREAK_FREQUENCY_MAX = 45  # minutes
BREAK_DURATION_MIN = 60  # seconds
BREAK_DURATION_MAX = 180  # seconds
MAX_SESSION_HOURS = (4, 6)  # Random between 4-6 hours

# Mouse settings
MOUSE_SPEED = 1.0  # Multiplier for mouse movement speed
MISCLICK_CHANCE = 0.05  # 5% chance to misclick slightly

# Action delays (seconds)
ACTION_DELAY_MEAN = 0.15
ACTION_DELAY_STD = 0.05

# Detection thresholds
TEMPLATE_MATCH_THRESHOLD = 0.8
BANK_DETECTION_THRESHOLD = 0.15

# Logging
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARN, ERROR
VERBOSE = True
