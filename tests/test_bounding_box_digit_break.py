from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_digit_break():
    sample = Path(__file__).parent / "sample_digit_break.step"
    bb = bounding_box(sample)
    assert bb == (1.0, 2.0, 3.0, 1.0, 2.0, 3.0)
