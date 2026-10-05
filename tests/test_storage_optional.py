"""Storage and dialect tools import without their optional providers."""

import subprocess
import sys

import pytest


def test_optional_storage_modules_do_not_import_providers():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import pyunitwizard.dialects.cf; import pyunitwizard.storage.hdf5; assert 'cf_units' not in sys.modules; assert 'h5py' not in sys.modules",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_missing_cf_provider_has_an_installation_diagnostic(monkeypatch):
    import depdigest

    from pyunitwizard.dialects import cf

    monkeypatch.setattr(depdigest, "is_installed", lambda library: False)
    with pytest.raises(ModuleNotFoundError, match="cf-units"):
        cf.validate_unit("meter", "m")


def test_missing_hdf5_provider_has_an_installation_diagnostic(monkeypatch):
    import depdigest

    from pyunitwizard.storage import hdf5

    monkeypatch.setattr(depdigest, "is_installed", lambda library: False)
    with pytest.raises(ModuleNotFoundError, match="h5py"):
        hdf5.read(None)
