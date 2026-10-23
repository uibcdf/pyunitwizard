"""Exercise the docs CLI with controlled child outcomes and caller files (#118)."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "docs" / "execute_notebooks.py"


@pytest.mark.parametrize("names", [("success",), ("failure",), ("failure", "success")])
@pytest.mark.parametrize("selection", ["files", "directory"])
def test_batch_exit_preserves_logs_and_processes_every_notebook(tmp_path, names, selection):
    jupyter = tmp_path / "jupyter"
    jupyter.write_text(
        f"#!{sys.executable}\n"
        "import pathlib, sys\n"
        "notebook = pathlib.Path(sys.argv[-1])\n"
        "print('controlled execution: ' + notebook.stem)\n"
        "sys.exit(7 if notebook.stem == 'failure' else 0)\n"
    )
    jupyter.chmod(0o700)
    notebooks = [tmp_path / f"{name}.ipynb" for name in names]
    for notebook in notebooks:
        notebook.write_text("caller-owned notebook")
        notebook.with_suffix(".nbconvert.last_run").write_text("0")
    receipt = tmp_path / "caller-receipt.json"
    receipt.write_text("preserve caller evidence")
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *(map(str, notebooks) if selection == "files" else [str(tmp_path)])],
        cwd=tmp_path,
        env={**os.environ, "PATH": str(tmp_path) + os.pathsep + os.environ["PATH"]},
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == (1 if "failure" in names else 0), completed.stdout + completed.stderr
    for notebook in notebooks:
        assert notebook.read_text() == "caller-owned notebook"
        assert "controlled execution" in notebook.with_suffix(".nbconvert.log").read_text()
        assert notebook.with_suffix(".nbconvert.last_run").exists() is (notebook.stem != "failure")
    assert receipt.read_text() == "preserve caller evidence"
