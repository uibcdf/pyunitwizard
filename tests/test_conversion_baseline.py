"""New benchmark evidence must name the interpreter that actually ran it."""

import json
import platform
import subprocess
import sys
from pathlib import Path


def test_baseline_reports_the_actual_python_runtime():
    # The benchmark resets global policy; exercise it in a fresh process.
    script = """
import json
import runpy
benchmark = runpy.run_path('benchmarks/conversion_baseline.py')
print(json.dumps(benchmark['run_baseline'](iterations=1, repeats=1)))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(completed.stdout)
    assert report["python"] == platform.python_version()
    assert report["results"]
    assert report["results"].keys() == report["results_telemetry_disabled"].keys()
