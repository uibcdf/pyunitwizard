"""OpenFF remains optional, lazy, and unavailable with a clear Python 3.11 route."""

import subprocess
import sys

import pytest

from pyunitwizard.forms.api_openff_units import require_openff


def test_import_does_not_load_the_optional_openff_registry():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import pyunitwizard; import pyunitwizard.forms.api_openff_units; assert 'openff.units' not in sys.modules; assert 'pint' not in sys.modules",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_missing_or_unsupported_openff_has_an_installation_route(monkeypatch):
    if sys.version_info < (3, 12):
        with pytest.raises(ModuleNotFoundError, match="Python 3.12"):
            require_openff()
    else:
        import depdigest

        monkeypatch.setattr(depdigest, "is_installed", lambda name: False)
        with pytest.raises(ModuleNotFoundError, match="conda install.*openff-units"):
            require_openff()
