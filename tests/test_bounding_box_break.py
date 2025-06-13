from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_break_after_sign():
    sample = Path(__file__).parent / "sample_break.step"
    bb = bounding_box(sample)
    assert bb == (10.0, 0.2, 0.3, 10.0, 0.2, 0.3)
