# Crown CNC Estimator

Utilities for estimating CNC runtime and parsing STEP models.
The package can be installed in editable mode for development or as a
standard dependency.

```bash
pip install -e .
```

This installs the ``crown-cnc-estimator`` command-line interface.

The project includes a test suite based on `pytest` and a sample STEP file
in `tests/`.

## Usage

Calculate runtime:

```python
from crown_cnc_estimator import calculate_runtime

runtime = calculate_runtime(feed_rate=100, path_length=200)
print(runtime)  # 2.0 minutes
```

Parse a STEP file:

```python
from pathlib import Path
from crown_cnc_estimator import parse_step

count = parse_step(Path("example.step"))
print(count)
```

The CLI now organizes features into subcommands.
Compute a bounding box with rounding to the nearest 0.125&nbsp;inch
(3.175&nbsp;mm):

```bash
crown-cnc-estimator bounding-box tests/sample.step --units inch --material 1018
```

Other available subcommands are:

```bash
crown-cnc-estimator parse-step tests/sample.step
crown-cnc-estimator runtime 100 200
```

Run interactively to be prompted for arguments, or launch a small GUI:

```bash
crown-cnc-estimator interactive
crown-cnc-estimator gui
```

For a web-based interface, install `streamlit` and run the provided app:

```bash
streamlit run streamlit_app.py
```

## Running Tests

Install `pytest` if necessary and run:

```bash
pytest
```
