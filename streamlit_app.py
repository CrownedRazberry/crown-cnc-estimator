import streamlit as st
from pathlib import Path

from crown_cnc_estimator.runtime import calculate_runtime
from crown_cnc_estimator.step_parser import bounding_box
from crown_cnc_estimator.cli import MATERIALS, INCH_INC, MM_INC, round_up

st.title("Crown CNC Estimator")

mode = st.sidebar.selectbox(
    "Select mode",
    ("Bounding Box", "Runtime"),
)

if mode == "Bounding Box":
    st.header("Bounding Box")
    file = st.file_uploader("STEP file")
    units = st.selectbox("Units", ["metric", "inch"], index=0)
    material = st.selectbox("Material", list(MATERIALS), index=0)
    if file and st.button("Compute"):
        path = Path("uploaded.step")
        with path.open("wb") as f:
            f.write(file.getvalue())
        try:
            bb = bounding_box(path)
        except Exception as exc:
            st.error(str(exc))
        else:
            min_x, min_y, min_z, max_x, max_y, max_z = bb
            dims = (max_x - min_x, max_y - min_y, max_z - min_z)
            increment = INCH_INC if units == "inch" else MM_INC
            rounded = tuple(round_up(d, increment) for d in dims)
            st.text(f"Material: {MATERIALS[material]}")
            st.text(f"Units: {units}")
            st.text(f"Bounding box:\n  X: {rounded[0]}\n  Y: {rounded[1]}\n  Z: {rounded[2]}")
        finally:
            path.unlink(missing_ok=True)

elif mode == "Runtime":
    st.header("Runtime")
    feed_rate = st.number_input("Feed rate (units/min)", min_value=0.0, value=100.0)
    path_len = st.number_input("Path length (units)", min_value=0.0, value=200.0)
    if st.button("Calculate"):
        try:
            runtime = calculate_runtime(feed_rate, path_len)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.text(f"Estimated runtime: {runtime} minutes")
