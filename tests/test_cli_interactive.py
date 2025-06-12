import subprocess
import sys
from pathlib import Path


def test_interactive_subcommand():
    sample = Path(__file__).parent / "sample.step"
    inputs = f"{sample}\nmetric\n6061\n"
    cmd = [sys.executable, "-m", "crown_cnc_estimator.cli", "interactive"]
    result = subprocess.run(cmd, input=inputs, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Material: 6061 aluminum" in result.stdout
