"""Protect the cold-interpreter fixture lifetime, including timeout (#115)."""

from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

HARNESS = runpy.run_path(str(Path(__file__).with_name("test_concurrent_registry_construction.py")))
REAL_RUN = subprocess.run

STUBS = textwrap.dedent(
    """
    import json, os, pathlib, sys, tempfile, threading, types
    receipt = pathlib.Path(os.environ['RACE_RESOURCE_RECEIPT'])
    def record(root):
        receipt.write_text(json.dumps({'root': str(root)}))
    original_mkdtemp = tempfile.mkdtemp
    def marked_mkdtemp(*args, **kwargs):
        root = original_mkdtemp(*args, **kwargs)
        record(root)
        return root
    tempfile.mkdtemp = marked_mkdtemp
    if len(sys.argv) > 1:
        record(sys.argv[1])

    def configure(*args):
        # Both clients must still have their source while import threads run.
        root = pathlib.Path(json.loads(receipt.read_text())['root'])
        assert all((root / name / '__init__.py').exists()
                   for name in ('client_one', 'client_two'))
        if os.environ['RACE_RESOURCE_OUTCOME'] == 'failure':
            raise RuntimeError('controlled configuration failure')
        if os.environ['RACE_RESOURCE_OUTCOME'] == 'timeout':
            threading.Event().wait()
    module = types.ModuleType('pyunitwizard')
    module.configure = types.SimpleNamespace(
        has_active_policy=lambda: False,
        set_default_form=configure,
        set_default_parser=lambda *args: None,
        set_standard_units=lambda *args: None,
    )
    sys.modules['pyunitwizard'] = module
    """
)


def instrument(monkeypatch, tmp_path, outcome):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    receipt = tmp_path / "caller-receipt.json"
    monkeypatch.setattr(tempfile, "tempdir", str(workspace))
    children = []
    real_popen = subprocess.Popen

    def popen(*args, **kwargs):
        child = real_popen(*args, **kwargs)
        children.append(child)
        return child

    def run(command, **kwargs):
        assert command[:2] == [sys.executable, "-c"]
        assert kwargs == {"capture_output": True, "text": True, "timeout": 300}
        environment = dict(
            os.environ,
            TMPDIR=str(workspace),
            TEMP=str(workspace),
            TMP=str(workspace),
            RACE_RESOURCE_RECEIPT=str(receipt),
            RACE_RESOURCE_OUTCOME=outcome,
        )
        command = [*command]
        command[2] = STUBS + command[2]
        return REAL_RUN(
            command, capture_output=True, text=True, env=environment, timeout=1 if outcome == "timeout" else 10
        )

    monkeypatch.setattr(subprocess, "Popen", popen)
    monkeypatch.setattr(subprocess, "run", run)
    return workspace, receipt, children


@pytest.mark.parametrize("outcome", ["success", "failure", "timeout"])
def test_owned_clients_removed_after_child_outcome(monkeypatch, tmp_path, outcome):
    workspace, receipt, children = instrument(monkeypatch, tmp_path, outcome)
    if outcome == "failure":
        with pytest.raises(AssertionError, match="controlled configuration failure"):
            HARNESS["test_two_threads_may_configure_at_once"](0)
    elif outcome == "timeout":
        with pytest.raises(subprocess.TimeoutExpired):
            HARNESS["test_two_threads_may_configure_at_once"](0)
    else:
        HARNESS["test_two_threads_may_configure_at_once"](0)
    assert children and all(child.poll() is not None for child in children)
    assert receipt.exists(), "caller-owned evidence must survive"
    root = Path(json.loads(receipt.read_text())["root"])
    assert not root.exists()
    assert workspace.exists() and not list(workspace.iterdir())


@pytest.mark.parametrize("outcome", ["success", "failure"])
def test_removal_error_visible_after_child_finished(monkeypatch, tmp_path, outcome):
    workspace, receipt, children = instrument(monkeypatch, tmp_path, outcome)

    def remove(cls, name, **kwargs):
        assert children and all(child.poll() is not None for child in children)
        raise PermissionError("controlled removal failure")

    monkeypatch.setattr(tempfile.TemporaryDirectory, "_rmtree", classmethod(remove))
    with pytest.raises(PermissionError, match="controlled removal failure") as caught:
        HARNESS["test_two_threads_may_configure_at_once"](0)
    if outcome == "failure":
        assert isinstance(caught.value.__context__, AssertionError)
        assert "controlled configuration failure" in str(caught.value.__context__)
    assert receipt.exists() and list(workspace.iterdir())


def test_parent_cleans_after_process_cannot_start(monkeypatch, tmp_path):
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    seen = []

    def run(command, **kwargs):
        seen.extend(tmp_path.iterdir())
        raise OSError("controlled process start failure")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(OSError, match="controlled process start failure"):
        HARNESS["test_two_threads_may_configure_at_once"](0)
    assert seen, "parent must acquire its fixture before starting the child"
    assert not list(tmp_path.iterdir())
