"""Interactive HSV threshold calibration using OpenCV trackbars."""

from typing import Dict, Tuple

import cv2
import numpy as np


CALIBRATION_WINDOW = "HSV Calibration Controls"

# Beginner-friendly starting values that select a broad range of colors.
DEFAULT_HSV_VALUES = {
    "H Min": 0,
    "H Max": 179,
    "S Min": 100,
    "S Max": 255,
    "V Min": 100,
    "V Max": 255,
}


def _on_trackbar_change(_value: int) -> None:
    """Required OpenCV callback; values are read directly inside the loop."""


def initialize_calibration_window() -> None:
    """Create the calibration window and its six HSV trackbars."""
    cv2.namedWindow(CALIBRATION_WINDOW)

    for trackbar_name, starting_value in DEFAULT_HSV_VALUES.items():
        maximum = 179 if trackbar_name.startswith("H") else 255
        cv2.createTrackbar(
            trackbar_name,
            CALIBRATION_WINDOW,
            starting_value,
            maximum,
            _on_trackbar_change,
        )


def get_hsv_trackbar_values() -> Dict[str, int]:
    """Read the current lower and upper HSV values from the controls."""
    return {
        name: cv2.getTrackbarPos(name, CALIBRATION_WINDOW)
        for name in DEFAULT_HSV_VALUES
    }


def create_calibration_views(
    frame: np.ndarray, hsv_values: Dict[str, int]
) -> Tuple[np.ndarray, np.ndarray]:
    """Return the mask and masked result for a BGR webcam frame."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Hue (H) chooses the basic color on OpenCV's 0-179 color wheel.
    # Saturation (S) controls color intensity: low values look gray or pale.
    # Value (V) controls brightness: low values are dark, high values are bright.
    lower_bound = np.array(
        [hsv_values["H Min"], hsv_values["S Min"], hsv_values["V Min"]]
    )
    upper_bound = np.array(
        [hsv_values["H Max"], hsv_values["S Max"], hsv_values["V Max"]]
    )

    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return mask, result


def run_calibration(camera: cv2.VideoCapture) -> int:
    """Show live original, mask, and result views until the user presses Q."""
    initialize_calibration_window()

    while True:
        frame_was_read, frame = camera.read()
        if not frame_was_read:
            print("Error: Could not read a frame from the webcam.")
            return 1

        hsv_values = get_hsv_trackbar_values()
        mask, result = create_calibration_views(frame, hsv_values)

        cv2.imshow("Calibration - Original", frame)
        cv2.imshow("Calibration - HSV Mask", mask)
        cv2.imshow("Calibration - Result", result)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            return 0
