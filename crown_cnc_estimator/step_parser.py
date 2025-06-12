"""STEP file parsing utilities."""
from pathlib import Path


def parse_step(file_path: Path | str) -> int:
    """Return the number of data entries in the given STEP file."""
    path = Path(file_path)
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("#"):
                count += 1
    return count
