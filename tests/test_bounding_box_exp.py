from pathlib import Path
from crown_cnc_estimator.step_parser import bounding_box

def test_bounding_box_scientific_notation():
    sample = Path(__file__).parent / "sample_exp.step"
    bb = bounding_box(sample)
    assert bb == (0.5, -0.25, -0.35, 1.0, 2.0, 4.2)
