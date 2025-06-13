from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_d_exponent():
    sample = Path(__file__).parent / "sample_d.step"
    bb = bounding_box(sample)
    assert bb == (1.0, 2.0, -0.3, 1.0, 2.0, -0.3)
