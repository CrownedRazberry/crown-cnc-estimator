from crown_cnc_estimator.runtime import calculate_material_removal_rate
import pytest


def test_mrr_basic():
    assert calculate_material_removal_rate(100, 2, 0.5) == 100 * 2 * 0.5


def test_mrr_invalid_feed_rate():
    with pytest.raises(ValueError):
        calculate_material_removal_rate(0, 2, 0.5)


def test_mrr_negative_depth():
    with pytest.raises(ValueError):
        calculate_material_removal_rate(100, 2, -1)
