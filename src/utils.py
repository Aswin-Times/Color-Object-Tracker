"""Small utilities used by the Color Object Tracker."""

import time
from typing import Optional, Tuple


def calculate_fps(
    previous_time: Optional[float], current_time: Optional[float] = None
) -> Tuple[float, float]:
    """Return the current FPS and the timestamp to use on the next frame."""
    now = current_time if current_time is not None else time.perf_counter()

    if previous_time is None or now <= previous_time:
        return 0.0, now

    return 1.0 / (now - previous_time), now
