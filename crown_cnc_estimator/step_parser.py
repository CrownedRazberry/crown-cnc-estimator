"""STEP file parsing utilities."""

from __future__ import annotations

from pathlib import Path
import re

# Floating point numbers in STEP files may include scientific notation or omit
# a leading zero. Allow formats like ``1.``, ``.5`` and ``1.0E-3``.
_FLOAT_RE = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
_COORD_PATTERN = re.compile(rf"\(({_FLOAT_RE}),\s*({_FLOAT_RE}),\s*({_FLOAT_RE})\)")


def parse_step(file_path: Path | str) -> int:
    """Return the number of data entries in the given STEP file."""
    path = Path(file_path)
    count = 0
    # STEP files are typically plain text, but some models may include
    # non-UTF-8 characters. Ignore decode errors so such files can still be
    # processed without raising ``UnicodeDecodeError``.
    with path.open("r", encoding="utf-8", errors="ignore") as f:
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
    # Use ``errors='ignore'`` so files with a different encoding don't cause
    # a failure when reading.
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = _COORD_PATTERN.search(line)
            if match:
                xs.append(float(match.group(1)))
                ys.append(float(match.group(2)))
                zs.append(float(match.group(3)))
    if not xs:
        raise ValueError("No coordinate triples found in STEP file")
    return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)
