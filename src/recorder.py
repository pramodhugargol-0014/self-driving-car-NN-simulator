
import csv
import os


class DrivingRecorder:
    def __init__(self, file_path="data/driving_data.csv"):
        self.file_path = file_path

        file_exists = (
            os.path.exists(file_path)
            and os.path.getsize(file_path) > 0
        )

        self.file = open(
            file_path,
            "a",
            newline="",
            encoding="utf-8",
        )

        self.writer = csv.writer(self.file)

        if not file_exists:
            self.writer.writerow([
                "distance_front",
                "distance_left",
                "distance_right",
                "distance_back",
                "speed",
                "direction",
                "throttle",
                "steering"
            ])

        self.file.flush()

    def record(self, sensor_data, car, throttle, steering):
        self.writer.writerow([
            sensor_data["front"],
            sensor_data["left"],
            sensor_data["right"],
            sensor_data["back"],
            car["speed"],
            car["angle"] % 360,
            throttle,
            steering,
        ])

    def close(self):
        if self.file and not self.file.closed:
            self.file.close()
