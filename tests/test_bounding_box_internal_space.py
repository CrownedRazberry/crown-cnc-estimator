from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_internal_space():
    sample = Path(__file__).parent / "sample_internal_space.step"
    bb = bounding_box(sample)
    assert bb == (1.0, 2.0, -3.0, 1.0, 2.0, -3.0)
