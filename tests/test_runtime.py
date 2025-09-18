import pytest

from crown_cnc_estimator.runtime import (
    calculate_runtime,
    estimate_milling_runtime,
    MillingRuntimeEstimate,
)
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


def test_estimate_milling_runtime_breakdown():
    result = estimate_milling_runtime(
        stock_volume=1000,
        part_volume=400,
        roughing_mrr=10,
        finishing_volume=60,
        finishing_mrr=2,
        drilling_time=5,
        finishing_adder=1,
        overhead_time=4,
    )

    assert isinstance(result, MillingRuntimeEstimate)
    # Volumetric removal breakdown
    assert result.removal_volume == pytest.approx(600)
    assert result.rough_minutes == pytest.approx(54)
    assert result.finish_minutes == pytest.approx(31)
    assert result.minutes_per_part == pytest.approx(94)
    # Effective MRR: total removal divided by cutting time (rough + finish)
    assert result.effective_mrr == pytest.approx(600 / (54 + 31))


def test_estimate_milling_runtime_finishing_volume_guard():
    with pytest.raises(ValueError):
        estimate_milling_runtime(
            stock_volume=100,
            part_volume=10,
            roughing_mrr=5,
            finishing_volume=200,
        )


def test_estimate_milling_runtime_zero_removal():
    result = estimate_milling_runtime(
        stock_volume=100,
        part_volume=100,
        roughing_mrr=5,
        drilling_time=2,
        finishing_adder=0.5,
    )

    assert result.removal_volume == 0
    assert result.minutes_per_part == pytest.approx(2.5)
    assert result.rough_minutes == 0
    assert result.finish_minutes == pytest.approx(0.5)
