"""Installed-consumer source snapshots exclude ignored tools and themselves."""

import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "integration/test_function_citation_provider.py"


def test_nested_installed_source_snapshot_preserves_current_nonignored_inputs(tmp_path, monkeypatch):
    root = tmp_path / "checkout"
    root.mkdir()
    (root / "pyunitwizard").mkdir()
    (root / ".gitignore").write_text(".governance-tools/\n.env\n")
    tracked = root / "pyunitwizard/current.py"
    tracked.write_text("# original\n")
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    tracked.write_text("# current working-tree source\n")
    (root / "pyunitwizard/new.py").write_text("# new nonignored source\n")
    (root / ".env").write_text("ignored private fixture marker\n")
    temporary = root / ".governance-tools/receiving"
    temporary.mkdir(parents=True)
    (temporary / "ignored.txt").write_text("must not be snapshotted\n")

    fixture = runpy.run_path(str(FIXTURE))["test_normally_installed_consumer_outside_checkout"]
    fixture.__globals__["__file__"] = str(root / "tests/integration/test_function_citation_provider.py")
    native_run = subprocess.run

    class SnapshotComplete(Exception):
        pass

    def stop_before_build(arguments, **kwargs):
        if arguments[0] == "git":
            return native_run(arguments, **kwargs)
        assert arguments[:3] == [sys.executable, "-m", "venv"]
        raise SnapshotComplete

    def refuse_unbounded_tree(*args, **kwargs):
        raise AssertionError("snapshot traversed its own checkout instead of finite source inputs")

    monkeypatch.setattr(subprocess, "run", stop_before_build)
    monkeypatch.setattr(shutil, "copytree", refuse_unbounded_tree)
    with pytest.raises(SnapshotComplete):
        fixture(None, temporary)
    snapshot = temporary / "producer-source"
    assert (snapshot / "pyunitwizard/current.py").read_bytes() == tracked.read_bytes()
    assert (snapshot / "pyunitwizard/new.py").read_bytes() == (root / "pyunitwizard/new.py").read_bytes()
    assert not (snapshot / ".governance-tools").exists()
    assert not (snapshot / ".env").exists()
    assert not (snapshot / ".git").exists()
