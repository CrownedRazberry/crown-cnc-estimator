import subprocess
import sys


def test_runtime_subcommand():
    cmd = [sys.executable, "-m", "crown_cnc_estimator.cli", "runtime", "100", "200"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Estimated runtime: 2.0 minutes" in result.stdout
