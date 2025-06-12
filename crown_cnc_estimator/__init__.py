"""Top-level package for Crown CNC Estimator."""

from .runtime import calculate_runtime
from .step_parser import parse_step, bounding_box

APP_NAME = "Crown CNC Estimator"
__all__ = ["calculate_runtime", "parse_step", "bounding_box", "APP_NAME"]
__version__ = "0.1.0"
