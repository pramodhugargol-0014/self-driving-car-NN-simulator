import pygame
from src import config

def draw_track(screen):
    screen.fill(config.GRASS)

    # Outer road boundary
    pygame.draw.ellipse(
        screen,
        config.ROAD,
        (
            config.CX - config.OUTER_RX,
            config.CY - config.OUTER_RY,
            config.OUTER_RX * 2,
            config.OUTER_RY * 2,
        ),
    )

    # Inner grass island
    pygame.draw.ellipse(
        screen,
        config.GRASS,
        (
            config.CX - config.INNER_RX,
            config.CY - config.INNER_RY,
            config.INNER_RX * 2,
            config.INNER_RY * 2,
        ),
    )

    # Outer track boundary
    pygame.draw.ellipse(
        screen,
        config.WHITE,
        (
            config.CX - config.OUTER_RX,
            config.CY - config.OUTER_RY,
            config.OUTER_RX * 2,
            config.OUTER_RY * 2,
        ),
        3,
    )

    # Inner track boundary
    pygame.draw.ellipse(
        screen,
        config.WHITE,
        (
            config.CX - config.INNER_RX,
            config.CY - config.INNER_RY,
            config.INNER_RX * 2,
            config.INNER_RY * 2,
        ),
        3,
    )


def draw_start_finish(screen, font):
    y = int(config.START_FINISH_Y)
    x1 = int(config.START_FINISH_X - config.START_LINE_LENGTH / 2)
    x2 = int(config.START_FINISH_X + config.START_LINE_LENGTH / 2)

    pygame.draw.line(
        screen,
        config.WHITE,
        (x1, y),
        (x2, y),
        5,
    )

    draw_text(
        screen,
        font,
        "START / FINISH",
        x1,
        y - 25,
        config.WHITE,
    )


def draw_text(screen, font, text, x, y, color=config.WHITE):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def update_laps(car, dt):
    car["total_time"] += dt
    car["lap_time"] += dt

    previous_x = car["previous_x"]
    previous_y = car["previous_y"]
    current_x = car["x"]
    current_y = car["y"]

    line_y = config.START_FINISH_Y
    half_length = config.START_LINE_LENGTH / 2

    crossed_line = (
        (previous_y < line_y <= current_y)
        or (previous_y > line_y >= current_y)
    )

    if crossed_line:
        fraction = (
            (line_y - previous_y)
            / (current_y - previous_y)
        )

        crossing_x = previous_x + fraction * (
            current_x - previous_x
        )

        line_start = config.START_FINISH_X - half_length
        line_end = config.START_FINISH_X + half_length

        if line_start <= crossing_x <= line_end:
            car["laps"] += 1
            car["last_lap_time"] = car["lap_time"]
            car["lap_time"] = 0.0

            print(f"Lap completed: {car['laps']}")

    car["previous_x"] = current_x
    car["previous_y"] = current_y