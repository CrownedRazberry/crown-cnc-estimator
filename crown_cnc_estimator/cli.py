from __future__ import annotations

import argparse
from pathlib import Path

from .step_parser import bounding_box
from . import APP_NAME

INCH_INC = 0.125
MM_INC = 3.175  # 0.125 inch in mm

MATERIALS = {
    "6061": "6061 aluminum",
    "1018": "1018 steel",
    "304": "304 stainless",
}

def round_up(value: float, increment: float) -> float:
    """Round ``value`` up to the nearest multiple of ``increment``."""
    import math
    return math.ceil(value / increment) * increment


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=f"{APP_NAME} CLI")
    parser.add_argument("file", type=Path, help="STEP file to analyze")
    parser.add_argument(
        "--units",
        choices=["metric", "inch"],
        default="metric",
        help="Units used in the STEP file",
    )
    parser.add_argument(
        "--material",
        choices=list(MATERIALS),
        default="6061",
        help="Material type",
    )
    args = parser.parse_args(argv)

    bb = bounding_box(args.file)
    min_x, min_y, min_z, max_x, max_y, max_z = bb
    dims = (max_x - min_x, max_y - min_y, max_z - min_z)

    increment = INCH_INC if args.units == "inch" else MM_INC
    rounded_dims = tuple(round_up(d, increment) for d in dims)

    print(f"Material: {MATERIALS[args.material]}")
    print(f"Units: {args.units}")
    print(f"Bounding box: {rounded_dims[0]} x {rounded_dims[1]} x {rounded_dims[2]}")


if __name__ == "__main__":
    main()
