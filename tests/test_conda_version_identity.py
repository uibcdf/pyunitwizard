"""Guard exact PyUnitWizard version identity in the Conda artifact."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FREEZER = ROOT / "devtools" / "conda-build" / "freeze_project_version.py"


def _freezer_module():
    spec = importlib.util.spec_from_file_location("freeze_project_version", FREEZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_freezer_writes_one_exact_version_source(tmp_path):
    shutil.copy2(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    package = tmp_path / "pyunitwizard"
    package.mkdir()

    _freezer_module().freeze_project_version(tmp_path, "0.26.0")

    pyproject = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.26.0"' in pyproject
    assert 'dynamic = ["version"]' not in pyproject
    assert "[tool.versioningit" not in pyproject
    assert (package / "_version.py").read_text(
        encoding="utf-8"
    ) == '__version__ = "0.26.0"\n'


def test_freezer_rejects_an_untrusted_version(tmp_path):
    with pytest.raises(ValueError, match="Invalid package version"):
        _freezer_module().freeze_project_version(tmp_path, '0.26.0"; echo unsafe')


def test_conda_build_freezes_and_checks_the_exact_version():
    build_script = (ROOT / "devtools" / "conda-build" / "build.sh").read_text(
        encoding="utf-8"
    )
    assert build_script.index("freeze_project_version.py") < build_script.index(
        "pip install"
    )

    recipe = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    assert "m.version('pyunitwizard') == os.environ['PKG_VERSION']" in recipe
    assert "puw.__version__ == os.environ['PKG_VERSION']" in recipe
