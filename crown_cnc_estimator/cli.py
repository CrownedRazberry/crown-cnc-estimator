from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .step_parser import bounding_box
from .runtime import calculate_runtime
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

def _bounding_box_cmd(args: argparse.Namespace) -> None:
    if not args.file.exists():
        sys.exit(f"File not found: {args.file}")
    bb = bounding_box(args.file)
    min_x, min_y, min_z, max_x, max_y, max_z = bb
    dims = (max_x - min_x, max_y - min_y, max_z - min_z)

    increment = INCH_INC if args.units == "inch" else MM_INC
    rounded = tuple(round_up(d, increment) for d in dims)

    print(f"Material: {MATERIALS[args.material]}")
    print(f"Units: {args.units}")
    print("Bounding box:")
    print(f"  X: {rounded[0]}")
    print(f"  Y: {rounded[1]}")
    print(f"  Z: {rounded[2]}")


def _runtime_cmd(args: argparse.Namespace) -> None:
    try:
        runtime = calculate_runtime(args.feed_rate, args.path_length)
    except ValueError as exc:
        sys.exit(str(exc))
    print(f"Estimated runtime: {runtime} minutes")


def _interactive_cmd(_: argparse.Namespace) -> None:
    file_path = Path(input("STEP file path: ").strip())
    while not file_path.exists():
        print("File does not exist. Try again.")
        file_path = Path(input("STEP file path: ").strip())

    units = input("Units (metric/inch) [metric]: ").strip() or "metric"
    while units not in {"metric", "inch"}:
        print("Units must be 'metric' or 'inch'.")
        units = input("Units (metric/inch) [metric]: ").strip() or "metric"

    material = input("Material (6061/1018/304) [6061]: ").strip() or "6061"
    while material not in MATERIALS:
        print(f"Material must be one of: {', '.join(MATERIALS)}")
        material = input("Material (6061/1018/304) [6061]: ").strip() or "6061"

    _bounding_box_cmd(argparse.Namespace(file=file_path, units=units, material=material))


def _gui_cmd(_: argparse.Namespace) -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    def browse() -> None:
        path = filedialog.askopenfilename(title="Select STEP file")
        if path:
            file_var.set(path)

    def compute() -> None:
        fp = Path(file_var.get())
        if not fp.exists():
            messagebox.showerror("Error", "File does not exist")
            return
        args = argparse.Namespace(file=fp, units=units_var.get(), material=mat_var.get())
        try:
            bb = bounding_box(fp)
        except Exception as exc:  # pragma: no cover - GUI errors
            messagebox.showerror("Error", str(exc))
            return
        min_x, min_y, min_z, max_x, max_y, max_z = bb
        dims = (max_x - min_x, max_y - min_y, max_z - min_z)
        increment = INCH_INC if args.units == "inch" else MM_INC
        rounded = tuple(round_up(d, increment) for d in dims)
        msg = (
            f"Material: {MATERIALS[args.material]}\n"
            f"Units: {args.units}\n"
            f"Bounding box:\n  X: {rounded[0]}\n  Y: {rounded[1]}\n  Z: {rounded[2]}"
        )
        messagebox.showinfo("Result", msg)

    root = tk.Tk()
    root.title(APP_NAME)

    tk.Label(root, text="STEP File:").grid(row=0, column=0, sticky="w")
    file_var = tk.StringVar()
    tk.Entry(root, textvariable=file_var, width=40).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=browse).grid(row=0, column=2)

    tk.Label(root, text="Units:").grid(row=1, column=0, sticky="w")
    units_var = tk.StringVar(value="metric")
    ttk.Combobox(root, textvariable=units_var, values=["metric", "inch"], state="readonly").grid(row=1, column=1)

    tk.Label(root, text="Material:").grid(row=2, column=0, sticky="w")
    mat_var = tk.StringVar(value="6061")
    ttk.Combobox(root, textvariable=mat_var, values=list(MATERIALS)).grid(row=2, column=1)

    tk.Button(root, text="Compute", command=compute).grid(row=3, column=1)
    root.mainloop()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} CLI",
        epilog="Examples:\n  crown-cnc-estimator bounding-box sample.step --units inch --material 1018",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bb_parser = subparsers.add_parser("bounding-box", help="Compute bounding box for a STEP file")
    bb_parser.add_argument("file", type=Path, help="STEP file to analyze")
    bb_parser.add_argument("--units", choices=["metric", "inch"], default="metric", help="Units used in the STEP file")
    bb_parser.add_argument("--material", choices=list(MATERIALS), default="6061", help="Material type")
    bb_parser.set_defaults(func=_bounding_box_cmd)

    runtime_parser = subparsers.add_parser("runtime", help="Calculate runtime from feed rate and path length")
    runtime_parser.add_argument("feed_rate", type=float, help="Feed rate (units/min)")
    runtime_parser.add_argument("path_length", type=float, help="Path length (units)")
    runtime_parser.set_defaults(func=_runtime_cmd)

    subparsers.add_parser("interactive", help="Interactive bounding box prompts").set_defaults(func=_interactive_cmd)
    subparsers.add_parser("gui", help="Launch graphical interface").set_defaults(func=_gui_cmd)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
