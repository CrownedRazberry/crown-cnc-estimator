from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_pre_exponent_space():
    sample = Path(__file__).parent / "sample_pre.step"
    bb = bounding_box(sample)
    assert bb == (10.0, 2.0, -3.0, 10.0, 2.0, -3.0)
