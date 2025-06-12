from pathlib import Path
import pytest

from crown_cnc_estimator.step_parser import parse_step


def test_parse_sample_step():
    sample = Path(__file__).parent / "sample.step"
    assert parse_step(sample) == 5


def test_parse_step_missing_file():
    missing = Path("non_existent.step")
    with pytest.raises(FileNotFoundError):
        parse_step(missing)


def test_parse_large_step(tmp_path: Path):
    sample = Path(__file__).parent / "sample.step"
    data = sample.read_text()
    large_file = tmp_path / "large.step"
    # create a larger file by repeating the data 10 times
    large_file.write_text(data * 10)
    expected_count = 5 * 10
    assert parse_step(large_file) == expected_count
