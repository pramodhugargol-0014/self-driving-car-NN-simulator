import pygame
from src import config

def reset_car():
    return {
        "x": config.CX + (config.OUTER_RX + config.INNER_RX) / 2,
        "y": config.CY,
        "angle": 90.0,
        "speed": 0.0,
        "crashed": False,
        "laps": 0,
        "previous_x": config.CX + (config.OUTER_RX + config.INNER_RX) / 2,
        "previous_y": config.CY,
        "lap_time": 0.0,
        "total_time": 0.0,
        "last_lap_time": 0.0,
        "has_started": True,
    }

def draw_car(screen, car):
    car_surface = pygame.Surface(
        (config.CAR_LENGTH, config.CAR_WIDTH),
        pygame.SRCALPHA,
    )

    pygame.draw.rect(
        car_surface,
        config.RED,
        (0, 0, config.CAR_LENGTH, config.CAR_WIDTH),
        border_radius=5,
    )

    # Front windscreen
    pygame.draw.rect(
        car_surface,
        config.BLUE,
        (
            config.CAR_LENGTH - 12,
            4,
            7,
            config.CAR_WIDTH - 8,
        ),
        border_radius=2,
    )

    rotated = pygame.transform.rotate(
        car_surface, car["angle"]
    )

    rect = rotated.get_rect(
        center=(int(car["x"]), int(car["y"]))
    )

    screen.blit(rotated, rect)