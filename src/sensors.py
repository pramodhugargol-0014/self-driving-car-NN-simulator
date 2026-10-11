import math
import pygame
from src import config


def on_road(x, y):
    """Return True when a point is inside the track ring."""
    outer = (
        ((x - config.CX) / config.OUTER_RX) ** 2
        + ((y - config.CY) / config.OUTER_RY) ** 2
    )

    inner = (
        ((x - config.CX) / config.INNER_RX) ** 2
        + ((y - config.CY) / config.INNER_RY) ** 2
    )

    return outer <= 1 and inner >= 1


def get_sensor(x, y, angle):
    """Cast a ray and return its measured distance and endpoint."""
    radians = math.radians(angle)
    dx = math.cos(radians)
    dy = -math.sin(radians)

    distance = 0

    while distance < config.SENSOR_RANGE:
        distance += config.SENSOR_STEP

        px = x + dx * distance
        py = y + dy * distance

        if not on_road(px, py):
            distance -= config.SENSOR_STEP
            px = x + dx * distance
            py = y + dy * distance
            break

    return distance, (int(px), int(py))


def draw_sensors(screen, car):
    for name, relative_angle in config.SENSOR_ANGLES.items():
        angle = car["angle"] + relative_angle

        _, endpoint = get_sensor(
            car["x"], car["y"], angle
        )

        pygame.draw.line(
            screen,
            config.YELLOW,
            (int(car["x"]), int(car["y"])),
            endpoint,
            2,
        )

        pygame.draw.circle(
            screen,
            config.YELLOW,
            endpoint,
            4,
        )