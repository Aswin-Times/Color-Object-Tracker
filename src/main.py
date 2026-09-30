"""Run the real-time Color Object Tracker."""

import argparse
import sys
from typing import Optional

import cv2

from color_detection import create_color_masks, detect_objects, draw_detection
from utils import calculate_fps


def initialize_camera(camera_index: int = 0) -> Optional[cv2.VideoCapture]:
    """Open a webcam and return it, or return None when it is unavailable."""
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        camera.release()
        return None

    return camera


def run_color_tracker(camera: cv2.VideoCapture) -> int:
    """Run the original four-color object detection mode."""
    previous_time = None

    while True:
        frame_was_read, frame = camera.read()
        if not frame_was_read:
            print("Error: Could not read a frame from the webcam.", file=sys.stderr)
            return 1

        # HSV separates color (Hue) from brightness, which makes selecting
        # colors more reliable than thresholding the original BGR image.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        masks = create_color_masks(hsv_frame)
        detections = detect_objects(masks)

        for detection in detections:
            draw_detection(frame, detection)

        fps, previous_time = calculate_fps(previous_time)
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Color Object Tracker - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            return 0


def parse_arguments() -> argparse.Namespace:
    """Read the optional mode selection from the command line."""
    parser = argparse.ArgumentParser(description="Track or calibrate HSV colors.")
    parser.add_argument(
        "--calibrate",
        action="store_true",
        help="open the interactive HSV calibration windows",
    )
    return parser.parse_args()


def main() -> int:
    """Open the webcam and start tracking or calibration mode."""
    arguments = parse_arguments()
    camera = initialize_camera()
    if camera is None:
        print(
            "Error: Could not open the default webcam. "
            "Check that it is connected and not being used by another app.",
            file=sys.stderr,
        )
        return 1

    try:
        if arguments.calibrate:
            # Imported only when needed to keep calibration separate from the
            # original tracker while sharing the same webcam setup and cleanup.
            from calibration import run_calibration

            return run_calibration(camera)

        return run_color_tracker(camera)
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    raise SystemExit(main())
