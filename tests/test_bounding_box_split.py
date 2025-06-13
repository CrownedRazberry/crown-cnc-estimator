from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_split_lines():
    sample = Path(__file__).parent / "sample_split.step"
    bb = bounding_box(sample)
    assert bb == (0.0, 1.0, 2.0, 0.0, 1.0, 2.0)
