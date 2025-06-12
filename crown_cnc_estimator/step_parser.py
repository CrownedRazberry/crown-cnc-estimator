"""STEP file parsing utilities."""

from __future__ import annotations

from pathlib import Path
import re

_COORD_PATTERN = re.compile(r"\((-?\d*\.?\d+),\s*(-?\d*\.?\d+),\s*(-?\d*\.?\d+)")


def parse_step(file_path: Path | str) -> int:
    """Return the number of data entries in the given STEP file."""
    path = Path(file_path)
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#"):
                count += 1
    return count


def bounding_box(file_path: Path | str) -> tuple[float, float, float, float, float, float]:
    """Return (min_x, min_y, min_z, max_x, max_y, max_z) of coordinates found."""
    path = Path(file_path)
    xs: list[float] = []
    ys: list[float] = []
    zs: list[float] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            match = _COORD_PATTERN.search(line)
            if match:
                xs.append(float(match.group(1)))
                ys.append(float(match.group(2)))
                zs.append(float(match.group(3)))
    if not xs:
        raise ValueError("No coordinate triples found in STEP file")
    return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)
