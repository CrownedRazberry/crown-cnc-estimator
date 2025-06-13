"""STEP file parsing utilities."""

from __future__ import annotations

from pathlib import Path
import re

# Floating point numbers in STEP files may include scientific notation or omit
# a leading zero. Some exporters also insert whitespace inside numbers or use
# ``D``/``d`` as the exponent marker. The regex therefore captures a broad set of
# numeric strings and any embedded whitespace is stripped before conversion.
# ``_FLOAT_RE`` matches floating point values possibly split across several
# lines or containing internal whitespace. It accepts an optional sign,
# a mantissa with or without a leading digit and a scientific exponent using
# either ``E`` or ``D`` notation. Any whitespace is stripped prior to
# conversion to ``float``.
_FLOAT_RE = r"""
    [+-]?                             # optional sign
    (?:
        \d+(?:\s*\.\s*\d*)?       # digits with optional decimal part
        |                             # or
        \.?\s*\d+                    # leading decimal point
    )
    (?:\s*[eEdD]\s*[+-]?\s*\d+)?    # optional exponent, spaces allowed before
"""

# Match ``(x, y, z)`` allowing spaces or newlines almost anywhere within the
# numbers.
# ``_COORD_PATTERN`` captures ``(x, y, z)`` tuples where each value matches
# ``_FLOAT_RE``. Whitespace and line breaks are permitted almost anywhere inside
# the tuple.
_COORD_PATTERN = re.compile(
    rf"\(\s*({_FLOAT_RE})\s*,\s*({_FLOAT_RE})\s*,\s*({_FLOAT_RE})\s*\)",
    re.VERBOSE | re.IGNORECASE | re.MULTILINE,
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
