import math

import joblib
import keras
import numpy as np
import pygame

from src import config
from src.car import reset_car, draw_car
from src.recorder import DrivingRecorder
from src.sensors import on_road, get_sensor, draw_sensors
from src.track import draw_track, draw_start_finish, draw_text, update_laps
    

def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (config.WIDTH, config.HEIGHT)
    )
    pygame.display.set_caption("Self-Driving Car - Simulator")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    model = keras.models.load_model(
        "models/driving_model.keras"
    )
    scaler = joblib.load("models/scaler.pkl")

    control_mode = "manual"
    car = reset_car()
    recorder = DrivingRecorder()
    running = True

    while running:
        dt = min(clock.tick(60) / 1000.0, 0.05)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    car = reset_car()

                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_m:
                    control_mode = (
                        "manual"
                        if control_mode == "model"
                        else "model"
                    )

        if not running:
            break

        keys = pygame.key.get_pressed()

        # Read sensor distances
        sensor_data = {}

        for name, relative_angle in config.SENSOR_ANGLES.items():
            angle = car["angle"] + relative_angle

            distance, _ = get_sensor(
                car["x"], car["y"], angle
            )
            sensor_data[name] = distance

        # Select driving actions
        if control_mode == "manual":
            steering = (
                int(keys[pygame.K_LEFT])
                - int(keys[pygame.K_RIGHT])
            )

            throttle = int(keys[pygame.K_UP])
            
            braking = keys[pygame.K_DOWN]

            recorder.record(
                sensor_data, car, throttle, steering
            )

        else:
            inputs = np.array([[
                sensor_data["front"],
                sensor_data["left"],
                sensor_data["right"],
                sensor_data["back"],
                car["speed"],
                car["angle"] % 360,
            ]], dtype=np.float32)

            inputs = scaler.transform(inputs)

            throttle_pred, steering_pred = model.predict(
                inputs, verbose=0
            )

            throttle = int(throttle_pred[0][0] >= 0.5)

            if car["speed"] < 20:
                throttle = 1

            # Classes: 0 = right, 1 = straight, 2 = left
            steering_class = int(
                np.argmax(steering_pred[0])
            )

            steering = {
                0: -1,
                1: 0,
                2: 1,
            }[steering_class]

            braking = False

        # Update car physics
        if not car["crashed"]:

            if control_mode == "manual" and braking:
                car["speed"] -= config.BRAKING * dt
            elif throttle == 1:
                car["speed"] += config.ACCELERATION * dt
            else:
                car["speed"] -= 70 * dt

            car["speed"] = max(
                0,
                min(car["speed"], config.MAX_SPEED),
            )

            if car["speed"] > 0:
                car["angle"] += (
                    steering * config.TURN_RATE * dt
                )

            radians = math.radians(car["angle"])

            car["x"] += (
                math.cos(radians) * car["speed"] * dt
            )
            car["y"] -= (
                math.sin(radians) * car["speed"] * dt
            )
            # Check lap completion AFTER movement
            update_laps(car, dt)

            if not on_road(car["x"], car["y"]):
                car["crashed"] = True
                car["speed"] = 0

        # Render environment
        draw_track(screen)
        draw_start_finish(screen, font)
        draw_sensors(screen, car)
        draw_car(screen, car)

        draw_text(
            screen, font,
            f"Mode: {control_mode.upper()} (M to switch)",
            15, 15,
        )
        draw_text(
            screen, font,
            f"Speed: {car['speed']:.1f} px/s",
            15, 45,
        )
        draw_text(
            screen, font,
            f"Heading: {car['angle'] % 360:.1f} deg",
            15, 70,
        )
        draw_text(
            screen, font,
            f"Throttle: {throttle}",
            15, 95,
        )
        draw_text(
            screen, font,
            f"Steering: {steering}",
            15, 120,
        )

        draw_text(
            screen, font,
            f"Current lap: {car['lap_time']:.2f}s",
            config.WIDTH - 220, 45
        )

        draw_text(
        screen, font,
        f"Laps completed: {car['laps']}",
        config.WIDTH - 220, 15
            )

        if car["crashed"]:
            message = font.render(
                "OFF TRACK - Press R to restart",
                True, config.RED,
            )
            screen.blit(
                message,
                message.get_rect(
                    center=(
                        config.WIDTH // 2,
                        config.HEIGHT // 2,
                    )
                ),
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
