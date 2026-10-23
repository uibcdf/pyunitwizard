"""Run the real Conda build boundary without installing anything (#117)."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("version", "install_exit", "expected_exit", "installation_reached"),
    [("invalid-version", 0, 1, False), ("0.28.1", 19, 19, True), ("0.28.1", 0, 0, True)],
)
def test_build_preserves_prerequisite_and_installer_failures(
    tmp_path, version, install_exit, expected_exit, installation_reached
):
    source = tmp_path / "source"
    build = source / "devtools" / "conda-build"
    build.mkdir(parents=True)
    (source / "pyunitwizard").mkdir()
    shutil.copy2(ROOT / "pyproject.toml", source / "pyproject.toml")
    for filename in ("build.sh", "freeze_project_version.py"):
        shutil.copy2(ROOT / "devtools" / "conda-build" / filename, build / filename)
    caller = tmp_path / "caller-evidence.txt"
    caller.write_text("preserve caller evidence")
    interpreter = tmp_path / "python"
    interpreter.write_text(
        f"#!{sys.executable}\n"
        "import pathlib, subprocess, sys\n"
        "if sys.argv[1:3] == ['-m', 'pip']:\n"
        "    pathlib.Path('installer-called').write_text('installer boundary reached')\n"
        f"    sys.exit({install_exit})\n"
        f"sys.exit(subprocess.run([{sys.executable!r}, *sys.argv[1:]]).returncode)\n"
    )
    interpreter.chmod(0o700)
    completed = subprocess.run(
        ["bash", str(build / "build.sh")],
        cwd=source,
        env={**os.environ, "PYTHON": str(interpreter), "PKG_VERSION": version},
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == expected_exit, completed.stdout + completed.stderr
    assert (source / "installer-called").exists() is installation_reached
    assert ("Done" in completed.stdout) is (expected_exit == 0)
    assert caller.read_text() == "preserve caller evidence"
    if version == "0.28.1":
        assert (source / "pyunitwizard" / "_version.py").read_text() == '__version__ = "0.28.1"\n'
