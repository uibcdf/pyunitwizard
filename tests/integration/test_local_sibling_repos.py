from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest
import pyunitwizard as puw


REPO_ROOT = Path(__file__).resolve().parents[2]
SIBLING_ARGDIGEST = REPO_ROOT.parent / "argdigest"
SIBLING_DEPDIGEST = REPO_ROOT.parent / "depdigest"
SIBLING_SMONITOR = REPO_ROOT.parent / "smonitor"


def _siblings_available() -> bool:
    return SIBLING_ARGDIGEST.exists() and SIBLING_DEPDIGEST.exists() and SIBLING_SMONITOR.exists()


@contextmanager
def _prepend_paths(paths: list[Path]):
    original = list(sys.path)
    try:
        for path in reversed(paths):
            sys.path.insert(0, str(path))
        yield
    finally:
        sys.path[:] = original


@contextmanager
def _force_fresh_imports(packages: list[str]):
    removed = {}
    try:
        for package in packages:
            for key in list(sys.modules):
                if key == package or key.startswith(f"{package}."):
                    removed[key] = sys.modules.pop(key)
        yield
    finally:
        sys.modules.update(removed)


@pytest.mark.skipif(not _siblings_available(), reason="Sibling repos are not available in this environment")
def test_local_sibling_import_precedence_and_basic_contracts():
    with _prepend_paths([SIBLING_ARGDIGEST, SIBLING_DEPDIGEST, SIBLING_SMONITOR]), _force_fresh_imports(
        ["argdigest", "depdigest", "smonitor"]
    ):
        argdigest = importlib.import_module("argdigest")
        depdigest = importlib.import_module("depdigest")
        smonitor = importlib.import_module("smonitor")

        assert str(Path(argdigest.__file__).resolve()).startswith(str(SIBLING_ARGDIGEST.resolve()))
        assert str(Path(depdigest.__file__).resolve()).startswith(str(SIBLING_DEPDIGEST.resolve()))
        assert str(Path(smonitor.__file__).resolve()).startswith(str(SIBLING_SMONITOR.resolve()))

    payload = depdigest.get_info("pyunitwizard", format="dict")
    assert payload["module_path"] == "pyunitwizard"
    assert "dependencies" in payload

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    q = puw.quantity(1.0, "meter")
    assert puw.to_string(q) == "1.0 meter"
