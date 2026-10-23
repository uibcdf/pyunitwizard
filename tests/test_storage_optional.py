"""Storage and dialect tools import without their optional providers."""

import subprocess
import sys

import pytest


def test_optional_storage_modules_do_not_import_providers():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import pyunitwizard.dialects.cf; import pyunitwizard.storage.hdf5; import pyunitwizard.storage.zarr; import pyunitwizard.storage.arrow; assert not {'cf_units', 'h5py', 'zarr', 'pyarrow'} & set(sys.modules)",
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


@pytest.mark.parametrize("name", ["zarr", "arrow"])
def test_missing_storage_provider_has_an_installation_diagnostic(monkeypatch, name):
    import importlib

    import depdigest

    module = importlib.import_module("pyunitwizard.storage." + name)
    monkeypatch.setattr(depdigest, "is_installed", lambda library: False)
    with pytest.raises(ModuleNotFoundError, match="zarr|pyarrow"):
        module.read(None, unit="nm")


@pytest.mark.parametrize("name,provider", [("zarr", "zarr"), ("arrow", "pyarrow")])
def test_transitive_provider_failure_is_not_reported_as_absence(monkeypatch, name, provider):
    import builtins
    import importlib

    import depdigest

    module = importlib.import_module("pyunitwizard.storage." + name)
    original = builtins.__import__
    monkeypatch.setattr(depdigest, "is_installed", lambda library: True)

    def fail(child, *args, **kwargs):
        if child == provider:
            raise ModuleNotFoundError("injected transitive dependency failure", name="provider_child")
        return original(child, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fail)
    with pytest.raises(ModuleNotFoundError, match="transitive") as captured:
        module.read(None, unit="nm")
    assert captured.value.name == "provider_child"
