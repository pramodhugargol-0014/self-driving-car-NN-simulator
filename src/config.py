WIDTH, HEIGHT = 1000, 700

CONTROL_MODE = "manual"  # "manual" or "model"

# Colors
GRASS = (45, 125, 55)
ROAD = (65, 65, 65)
WHITE = (240, 240, 240)
RED = (220, 45, 45)
YELLOW = (255, 220, 40)
BLUE = (60, 180, 255)

# Track geometry
CX, CY = WIDTH // 2, HEIGHT // 2
OUTER_RX, OUTER_RY = 430, 290
INNER_RX, INNER_RY = 270, 130

# Car parameters
CAR_LENGTH = 36
CAR_WIDTH = 22
MAX_SPEED = 260.0
ACCELERATION = 220.0
BRAKING = 300.0
TURN_RATE = 150.0

# Sensor parameters
SENSOR_RANGE = 300
SENSOR_STEP = 2
SENSOR_ANGLES = {
    "front": 0,
    "left": 90,
    "right": -90,
    "back": 180,
}

# Start/finish line
START_FINISH_X = CX + (OUTER_RY + INNER_RY) / 2 + 140
START_FINISH_Y = CY
START_LINE_LENGTH = 150