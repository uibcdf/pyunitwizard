"""Guard the actual autosummary cleaner's disposal boundary (#116)."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "docs" / "clean_api.py"


def cleaner():
    spec = importlib.util.spec_from_file_location("pyunitwizard_clean_api", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cleaner_removes_generated_tree_and_preserves_authored_pages(tmp_path):
    generated = tmp_path / "users" / "autosummary"
    generated.mkdir(parents=True)
    (generated / "generated.rst").write_text("generated stub")
    authored = generated.parent / "index.rst"
    authored.write_text("caller-authored page")

    assert cleaner().delete_autosummary_dirs(tmp_path) == [generated]
    assert not generated.exists()
    assert authored.read_text() == "caller-authored page"


def test_cleaner_propagates_removal_failure(tmp_path, monkeypatch):
    generated = tmp_path / "autosummary"
    generated.mkdir()
    caller = tmp_path / "caller-receipt.json"
    caller.write_text("preserve evidence")
    module = cleaner()

    def reject(path):
        assert path == generated
        raise PermissionError("controlled cleanup failure")

    monkeypatch.setattr(module.shutil, "rmtree", reject)
    with pytest.raises(PermissionError, match="controlled cleanup failure"):
        module.delete_autosummary_dirs(tmp_path)
    assert generated.exists()
    assert caller.read_text() == "preserve evidence"


def test_cleaner_missing_generated_root_is_a_noop(tmp_path):
    assert cleaner().delete_autosummary_dirs(tmp_path / "absent") == []
