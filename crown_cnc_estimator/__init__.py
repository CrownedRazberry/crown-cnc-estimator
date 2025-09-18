"""Top-level package for Crown CNC Estimator."""

from .runtime import calculate_runtime
from .step_parser import bounding_box

APP_NAME = "Crown CNC Estimator"
__all__ = ["calculate_runtime", "bounding_box", "APP_NAME"]
__version__ = "0.1.0"
