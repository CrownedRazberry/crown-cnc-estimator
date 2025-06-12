from pathlib import Path

from crown_cnc_estimator.step_parser import bounding_box


def test_bounding_box_sample_metric():
    sample = Path(__file__).parent / "sample.step"
    bb = bounding_box(sample)
    assert bb == (0.0, 0.0, 0.0, 1.0, 0.0, 1.0)
