from pathlib import Path

from crown_cnc_estimator.step_parser import parse_step


def test_parse_sample_step():
    sample = Path(__file__).parent / "sample.step"
    assert parse_step(sample) == 5
