from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SIBLING_PYW = REPO_ROOT.parent / "pyunitwizard"
SIBLING_ARG = REPO_ROOT.parent / "argdigest"
SIBLING_DEP = REPO_ROOT.parent / "depdigest"
SIBLING_SMON = REPO_ROOT.parent / "smonitor"


def _siblings_available() -> bool:
    return all(path.exists() for path in [SIBLING_PYW, SIBLING_ARG, SIBLING_DEP, SIBLING_SMON])


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
def test_collective_error_path_emits_contract_signal_and_dependency_hints():
    with _prepend_paths([SIBLING_PYW, SIBLING_ARG, SIBLING_DEP, SIBLING_SMON]), _force_fresh_imports(
        ["pyunitwizard", "argdigest", "depdigest", "smonitor"]
    ):
        puw = importlib.import_module("pyunitwizard")
        argdigest = importlib.import_module("argdigest")
        depdigest = importlib.import_module("depdigest")
        smonitor = importlib.import_module("smonitor")
        puw_support = importlib.import_module("argdigest.contrib.pyunitwizard_support")

        manager = smonitor.get_manager()
        manager.configure(level="DEBUG", event_buffer_size=400)

        puw.configure.reset()
        puw.configure.load_library(["pint"])
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")

        @argdigest.arg_digest.map(
            distance={
                "kind": "quantity",
                "rules": [puw_support.check(dimensionality={"[L]": 1})],
            }
        )
        def _accept_distance(distance):
            return distance

        start = len(manager.recent_events())
        wrong_distance = puw.quantity(1.0, "picosecond", form="pint")

        with pytest.raises(argdigest.DigestValueError):
            _accept_distance(wrong_distance)

        recent = manager.recent_events()[start:]
        assert any((event.get("code") or "").startswith(("ARG-", "PUW-")) for event in recent)

        payload = depdigest.get_info("pyunitwizard", format="dict")
        dependencies = payload.get("dependencies", [])
        pint_rows = [item for item in dependencies if item.get("library") == "pint"]
        assert pint_rows
        assert "install" in pint_rows[0]
