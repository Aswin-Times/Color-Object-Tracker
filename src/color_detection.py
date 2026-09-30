"""Color masking and contour-based object detection helpers."""

from typing import Dict, List, Tuple

import cv2
import numpy as np


# OpenCV represents Hue on a 0-179 scale. Red wraps around that scale, so it
# needs two ranges. Saturation and Value minimums reject pale or dark pixels.
COLOR_RANGES = {
    "Red": [
        (np.array([0, 120, 70]), np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([179, 255, 255])),
    ],
    "Green": [(np.array([35, 70, 70]), np.array([85, 255, 255]))],
    "Blue": [(np.array([90, 80, 70]), np.array([130, 255, 255]))],
    "Yellow": [(np.array([20, 100, 100]), np.array([35, 255, 255]))],
}

# Drawing colors use OpenCV's BGR order.
DISPLAY_COLORS = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
}


def create_color_masks(hsv_frame: np.ndarray) -> Dict[str, np.ndarray]:
    """Create a cleaned binary mask for every configured color."""
    masks: Dict[str, np.ndarray] = {}
    kernel = np.ones((5, 5), dtype=np.uint8)

    for color_name, hsv_ranges in COLOR_RANGES.items():
        mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)

        for lower_bound, upper_bound in hsv_ranges:
            mask = cv2.bitwise_or(
                mask, cv2.inRange(hsv_frame, lower_bound, upper_bound)
            )

        # Opening removes isolated dots; closing fills small holes in objects.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        masks[color_name] = mask

    return masks


def detect_objects(
    masks: Dict[str, np.ndarray], minimum_area: float = 500.0
) -> List[dict]:
    """Find object outlines in masks and return useful detection information."""
    detections = []

    for color_name, mask in masks.items():
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < minimum_area:
                continue

            x, y, width, height = cv2.boundingRect(contour)
            center = (x + width // 2, y + height // 2)
            detections.append(
                {
                    "color": color_name,
                    "bounding_box": (x, y, width, height),
                    "center": center,
                    "area": area,
                }
            )

    return detections


def draw_detection(frame: np.ndarray, detection: dict) -> None:
    """Draw one object's bounding box, center, color, and coordinates."""
    color_name = detection["color"]
    x, y, width, height = detection["bounding_box"]
    center_x, center_y = detection["center"]
    drawing_color: Tuple[int, int, int] = DISPLAY_COLORS[color_name]

    cv2.rectangle(frame, (x, y), (x + width, y + height), drawing_color, 2)
    cv2.circle(frame, (center_x, center_y), 5, drawing_color, -1)

    label = f"{color_name} ({center_x}, {center_y})"
    text_y = max(y - 10, 20)
    cv2.putText(
        frame,
        label,
        (x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        drawing_color,
        2,
        cv2.LINE_AA,
    )
