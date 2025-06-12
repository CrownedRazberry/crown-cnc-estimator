from pathlib import Path
import subprocess
import sys


def test_parse_step_subcommand():
    sample = Path(__file__).parent / "sample.step"
    cmd = [sys.executable, "-m", "crown_cnc_estimator.cli", "parse-step", str(sample)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Entities: 5" in result.stdout


def test_runtime_subcommand():
    cmd = [sys.executable, "-m", "crown_cnc_estimator.cli", "runtime", "100", "200"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Estimated runtime: 2.0 minutes" in result.stdout
