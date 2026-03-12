import numpy as np
import pytest

import pyunitwizard as puw


def test_to_nanometers_converts_pint_quantity():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    quantity = puw.quantity(1.0, "meter", form="pint")
    output = puw.to_nanometers(quantity)

    assert puw.get_unit(output) == "nanometer"
    assert puw.get_value(output) == pytest.approx(np.float64(1e9))


def test_to_picoseconds_converts_pint_quantity():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    quantity = puw.quantity(1.0, "nanosecond", form="pint")
    output = puw.to_picoseconds(quantity)

    assert puw.get_unit(output) == "picosecond"
    assert puw.get_value(output) == pytest.approx(np.float64(1000.0))


def test_to_kelvin_preserves_string_quantity_in_kelvin():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_parser("pint")

    output = puw.to_kelvin("274.15 kelvin")

    assert output == "274.15 kelvin"


def test_specialized_passthrough_for_plain_ndarray():
    array = np.array([1.0, 2.0, 3.0], dtype=np.float64)

    assert puw.to_nanometers(array) is array
    assert puw.to_picoseconds(array) is array
    assert puw.to_kelvin(array) is array


def test_reset_clears_specialized_target_unit_cache():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    quantity = puw.quantity(1.0, "meter", form="pint")
    puw.to_nanometers(quantity)

    from pyunitwizard.api.specialized import _SPECIALIZED_TARGET_UNIT_CACHE

    assert _SPECIALIZED_TARGET_UNIT_CACHE

    puw.configure.reset()

    assert _SPECIALIZED_TARGET_UNIT_CACHE == {}
