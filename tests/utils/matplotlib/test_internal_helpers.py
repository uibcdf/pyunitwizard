from types import SimpleNamespace

import numpy as np
import pytest

import pyunitwizard as puw
from tests.helpers import loaded_libraries

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.units as munits

from pyunitwizard.utils import matplotlib as puw_mpl


def test_iterable_values_helper_contract():
    assert puw_mpl._iterable_values([1, 2]) == [1, 2]
    assert puw_mpl._iterable_values((1, 2)) == (1, 2)
    assert puw_mpl._iterable_values(np.array([1, 2])) == [1, 2]
    assert puw_mpl._iterable_values(3.0) is None


def test_first_quantity_like_returns_none_for_plain_values():
    assert puw_mpl._first_quantity_like([1.0, 2.0, 3.0]) is None
    assert puw_mpl._first_quantity_like(2.0) is None


def test_setup_matplotlib_registers_and_unregisters_types(monkeypatch):
    class DummyQuantity:
        pass

    monkeypatch.setattr(puw_mpl, "_discover_mpl_types", lambda: (DummyQuantity,))

    puw_mpl.setup_matplotlib(enable=True)
    assert DummyQuantity in munits.registry

    puw_mpl.setup_matplotlib(enable=False)
    assert DummyQuantity not in munits.registry


def test_plotting_context_restores_previous_registry(monkeypatch):
    class DummyQuantity:
        pass

    sentinel = object()
    munits.registry[DummyQuantity] = sentinel
    monkeypatch.setattr(puw_mpl, "_discover_mpl_types", lambda: (DummyQuantity,))

    with puw_mpl.plotting_context():
        assert DummyQuantity in munits.registry
        assert munits.registry[DummyQuantity] is not sentinel

    assert munits.registry[DummyQuantity] is sentinel
    munits.registry.pop(DummyQuantity, None)


def test_converter_default_units_and_axisinfo_branches():
    converter = puw_mpl._PyUnitWizardMplConverter()

    with loaded_libraries(["pint"]):
        length = puw.unit("meter", form="pint")
        time = puw.unit("second", form="pint")

        axis_without_unit = SimpleNamespace(units=None)
        resolved = converter.default_units(length, axis_without_unit)
        assert resolved == length

        axis_with_incompatible_unit = SimpleNamespace(units=time)
        with pytest.raises(ValueError):
            converter.default_units(length, axis_with_incompatible_unit)

        axis_info = converter.axisinfo(length, axis_without_unit)
        assert "meter" in axis_info.label
