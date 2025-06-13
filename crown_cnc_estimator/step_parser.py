"""STEP file parsing utilities."""

from __future__ import annotations

from pathlib import Path
import re

# Floating point numbers in STEP files may include scientific notation or omit
# a leading zero. Allow formats like ``1.``, ``.5`` and ``1.0E-3``.
# Include ``D`` or ``d`` as an exponent marker since some STEP files use that
# instead of ``E``. Allow formats like ``1.0D+3`` in addition to ``1.0E+3``.
_FLOAT_RE = (
    r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
    r"(?:[eEdD]\s*[+-]?\s*\d+)?"
)
# Allow optional whitespace before and after each comma and before the closing
# parenthesis so coordinates split across lines or with spaces still match.
_COORD_PATTERN = re.compile(
    rf"\(\s*({_FLOAT_RE})\s*,\s*({_FLOAT_RE})\s*,\s*({_FLOAT_RE})\s*\)"
)


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
    # Use ``errors='ignore'`` so files with a different encoding don't cause
    # a failure when reading.
    content = path.read_text(encoding="utf-8", errors="ignore")

    coords = _COORD_PATTERN.findall(content)
    if not coords:
        raise ValueError("No coordinate triples found in STEP file")

    # ``float`` does not understand ``D`` as an exponent marker, so normalise
    # any occurrences to ``E`` before converting.
    def _to_float(val: str) -> float:
        cleaned = re.sub(r"\s+", "", val)
        return float(cleaned.replace("D", "E").replace("d", "E"))

    xs, ys, zs = zip(*((_to_float(x), _to_float(y), _to_float(z)) for x, y, z in coords))
    return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)
