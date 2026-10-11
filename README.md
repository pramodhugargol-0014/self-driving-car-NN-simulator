# Self-Driving Car Simulation

A 2D self-driving car simulation built with **Python**, **Pygame**, and
a **neural network**. The project provides a race-track environment,
virtual distance sensors, driving-data collection, and model inference
for autonomous driving.

> **Project scope:** This is an experimental simulation for learning
> about supervised learning and autonomous-control concepts. It is not a
> real-world self-driving system.

## Features

-   **2D race track:** A fixed oval track rendered in Pygame.
-   **Car physics:** Basic acceleration, braking/coasting, steering, and
    speed limits.
-   **Virtual sensors:** Front, left, right, and rear distance
    measurements to the road boundary.
-   **Data collection:** Record sensor readings and vehicle state
    alongside driving actions in a CSV file.
-   **Neural-network inference:** Load a trained model and scaler and
    use the model's predictions during the game loop.
-   **Lap and collision logic:** Track lap progress and stop the car
    when it leaves the road.

## How it works

1.  Drive the car manually to collect example driving data.
2.  Save the recorded samples to a CSV file.
3.  Train and evaluate the neural network in Google Colab.
4.  Save the trained model and preprocessing scaler.
5.  Load them in the local simulation and use model predictions to
    control the car.

This workflow is a form of **supervised learning / behavioral cloning**:
the model learns to imitate the driving actions represented in the
collected examples.

## Model inputs

The model currently uses six input features:

  Feature            Description
  ------------------ ---------------------------------------------
  `distance_front`   Distance measured in front of the car
  `distance_left`    Distance measured to the left
  `distance_right`   Distance measured to the right
  `distance_back`    Distance measured behind the car
  `speed`            Current car speed
  `direction`        Current car heading, represented in degrees

The model's expected feature order and preprocessing must match the
training pipeline. The scaler saved during training is loaded for
inference.

**Driving outputs:** The model is used to predict driving actions such
as steering and throttle. The exact output format and thresholds are
defined by the training and inference code.

## Requirements

-   Python 3.10 or newer is a reasonable starting point; use the Python
    version compatible with the installed TensorFlow/Keras release.
-   Pygame
-   NumPy
-   TensorFlow/Keras
-   Joblib

Install the dependencies listed in the project:

``` bash
python -m pip install -r requirements.txt
```

## Run the simulation

From the project root, run:

``` bash
python game.py
```

If your entry-point file has a different name, run that file instead.

Use the control-mode setting in the code to switch between manual
driving and model-controlled driving. Make sure the model and scaler
paths match the files in your `models/` directory.

## Collect training data

1.  Start the game in manual-control mode.
2.  Drive around the track and use a range of steering and speed
    situations.
3.  Record the sensor values, speed, direction, and corresponding
    control actions.
4.  Save the CSV in `data/`.
5.  Inspect the data before training; avoid collecting only stationary
    or repetitive samples.

The CSV columns should correspond to the features and labels expected by
the training notebook. Keep feature names, feature order, units, and
preprocessing consistent between training and inference.

## Train the model

The model is trained in Google Colab using the collected CSV data.

1.  Upload the CSV dataset to Colab.
2.  Split the data into training, validation, and test sets.
3.  Fit preprocessing only on the training split, then apply the same
    scaler to the other splits.
4.  Train and evaluate the neural network.
5.  Save the model as `driving_model.keras` and the fitted scaler as
    `scaler.pkl`.
6.  Download both files into the local `models/` directory.

Do not fit a new scaler during game inference. Use the scaler fitted
during training.

## Current limitations

-   The simulation uses simplified 2D physics rather than a realistic
    vehicle model.
-   Sensors measure distances to the simulated road boundary; they are
    not camera-based object detectors.
-   The model can only learn situations represented in the training
    data.
-   Performance may vary with different speeds, starting positions,
    turns, and sensor readings.

## Possible next steps

-   Add multiple cars to the track and explore interactions between vehicles, 
    including collision avoidance and overtaking.
-   Add clearer evaluation metrics, such as successful laps, crashes,
    and average lap time.
-   Test the model from different starting positions and speeds.

## Technologies

-   Python
-   Pygame
-   NumPy
-   TensorFlow / Keras
-   Joblib
-   Google Colab

## Disclaimer

This project is for educational experimentation in a simulated
environment only. It is not designed or validated for controlling a real
vehicle.
