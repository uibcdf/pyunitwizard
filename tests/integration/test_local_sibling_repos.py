from __future__ import annotations

import importlib
import importlib.util
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


def _load_local_package_alias(repo_path: Path, package_name: str, alias: str):
    package_init = repo_path / package_name / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        alias,
        package_init,
        submodule_search_locations=[str(repo_path / package_name)],
    )
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.skipif(not _siblings_available(), reason="Sibling repos are not available in this environment")
def test_local_sibling_import_precedence_and_basic_contracts():
    argdigest_local = _load_local_package_alias(SIBLING_ARGDIGEST, "argdigest", "argdigest_local")
    depdigest_local = _load_local_package_alias(SIBLING_DEPDIGEST, "depdigest", "depdigest_local")
    smonitor_local = _load_local_package_alias(SIBLING_SMONITOR, "smonitor", "smonitor_local")

    assert str(Path(argdigest_local.__file__).resolve()).startswith(str(SIBLING_ARGDIGEST.resolve()))
    assert str(Path(depdigest_local.__file__).resolve()).startswith(str(SIBLING_DEPDIGEST.resolve()))
    assert str(Path(smonitor_local.__file__).resolve()).startswith(str(SIBLING_SMONITOR.resolve()))

    with _prepend_paths([SIBLING_ARGDIGEST, SIBLING_DEPDIGEST, SIBLING_SMONITOR]):
        depdigest = importlib.import_module("depdigest")

    payload = depdigest.get_info("pyunitwizard", format="dict")
    assert payload["module_path"] == "pyunitwizard"
    assert "dependencies" in payload

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    q = puw.quantity(1.0, "meter")
    assert puw.to_string(q) == "1.0 meter"
