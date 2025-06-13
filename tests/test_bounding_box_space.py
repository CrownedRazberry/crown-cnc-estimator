from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_space_exponent():
    sample = Path(__file__).parent / "sample_space.step"
    bb = bounding_box(sample)
    assert bb == (10.0, 0.2, -3.0, 10.0, 0.2, -3.0)
