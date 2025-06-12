import pytest

from crown_cnc_estimator.runtime import calculate_runtime
from crown_cnc_estimator import APP_NAME


def test_calculate_runtime_basic():
    assert calculate_runtime(100, 200) == 2

def test_calculate_runtime_zero_feed_rate():
    with pytest.raises(ValueError):
        calculate_runtime(0, 100)

def test_calculate_runtime_zero_path_length():
    assert calculate_runtime(100, 0) == 0


def test_calculate_runtime_negative_path_length():
    result = calculate_runtime(100, -50)
    assert result == -0.5


def test_app_name_constant():
    assert APP_NAME == "Crown CNC Estimator"
