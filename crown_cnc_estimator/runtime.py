"""Utilities for estimating CNC runtimes."""

from __future__ import annotations

from dataclasses import dataclass


def calculate_runtime(feed_rate: float, path_length: float) -> float:
    """Return runtime given ``feed_rate`` (units/min) and ``path_length`` (units)."""

    if feed_rate <= 0:
        raise ValueError("feed_rate must be greater than zero")
    return path_length / feed_rate


@dataclass(frozen=True)
class MillingRuntimeEstimate:
    """Structured result from :func:`estimate_milling_runtime`."""

    minutes_per_part: float
    rough_minutes: float
    finish_minutes: float
    drilling_minutes: float
    overhead_minutes: float
    removal_volume: float
    effective_mrr: float


def estimate_milling_runtime(
    stock_volume: float,
    part_volume: float,
    *,
    roughing_mrr: float,
    finishing_volume: float = 0.0,
    finishing_mrr: float | None = None,
    drilling_time: float = 0.0,
    finishing_adder: float = 0.0,
    overhead_time: float = 0.0,
) -> MillingRuntimeEstimate:
    """Estimate CNC milling runtime using a volumetric removal model.

    The calculation follows a "stock minus part equals removal volume" approach.
    The removal volume is split into roughing and finishing portions.  Roughing
    time is computed from the remaining material removal rate, and a finishing
    allowance can be converted to time with ``finishing_mrr``.  Additional time
    can be added for drilling, finishing passes, and overhead.

    Args:
        stock_volume: Volume of the starting stock.
        part_volume: Volume of the finished part.
        roughing_mrr: Effective material removal rate for roughing (volume/min).
        finishing_volume: Volume reserved for finishing operations.  Must not
            exceed the total removal volume.
        finishing_mrr: Material removal rate for finishing passes.  If omitted
            the roughing value is reused.
        drilling_time: Minutes added to account for drilling operations.
        finishing_adder: Extra finishing time (minutes) in addition to the
            volumetric allowance.
        overhead_time: Miscellaneous non-cutting time in minutes.

    Returns:
        A :class:`MillingRuntimeEstimate` summarising the breakdown.

    Raises:
        ValueError: If provided volumes or rates are inconsistent.
    """

    if stock_volume < 0:
        raise ValueError("stock_volume must be non-negative")
    if part_volume < 0:
        raise ValueError("part_volume must be non-negative")
    if roughing_mrr <= 0:
        raise ValueError("roughing_mrr must be greater than zero")
    if finishing_volume < 0:
        raise ValueError("finishing_volume must be non-negative")
    if drilling_time < 0:
        raise ValueError("drilling_time must be non-negative")
    if finishing_adder < 0:
        raise ValueError("finishing_adder must be non-negative")
    if overhead_time < 0:
        raise ValueError("overhead_time must be non-negative")

    removal_volume = max(stock_volume - part_volume, 0.0)
    if finishing_volume > removal_volume:
        raise ValueError("finishing_volume cannot exceed removal_volume")

    finishing_rate = roughing_mrr if finishing_mrr is None else finishing_mrr
    if finishing_rate <= 0:
        raise ValueError("finishing_mrr must be greater than zero")

    roughing_volume = removal_volume - finishing_volume
    rough_minutes = roughing_volume / roughing_mrr if roughing_volume else 0.0

    finishing_minutes = finishing_adder
    if finishing_volume:
        finishing_minutes += finishing_volume / finishing_rate

    minutes_per_part = rough_minutes + finishing_minutes + drilling_time + overhead_time

    cutting_minutes = rough_minutes + finishing_minutes
    if removal_volume and cutting_minutes:
        effective_mrr = removal_volume / cutting_minutes
    else:
        effective_mrr = 0.0

    return MillingRuntimeEstimate(
        minutes_per_part=minutes_per_part,
        rough_minutes=rough_minutes,
        finish_minutes=finishing_minutes,
        drilling_minutes=drilling_time,
        overhead_minutes=overhead_time,
        removal_volume=removal_volume,
        effective_mrr=effective_mrr,
    )
