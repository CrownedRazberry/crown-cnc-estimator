from pathlib import Path
import subprocess
import sys


def test_cli_runs(tmp_path):
    sample = Path(__file__).parent / "sample.step"
    cmd = [
        sys.executable,
        "-m",
        "crown_cnc_estimator.cli",
        "bounding-box",
        str(sample),
        "--units",
        "inch",
        "--material",
        "1018",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Material: 1018 steel" in result.stdout
