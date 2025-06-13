"""Top-level package for Crown CNC Estimator."""

from .runtime import calculate_runtime, calculate_material_removal_rate
from .step_parser import parse_step, bounding_box

APP_NAME = "Crown CNC Estimator"
__all__ = [
    "calculate_runtime",
    "calculate_material_removal_rate",
    "parse_step",
    "bounding_box",
    "APP_NAME",
]
__version__ = "0.1.0"
