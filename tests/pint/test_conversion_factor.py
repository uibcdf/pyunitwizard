import pytest

import pyunitwizard as puw
import pyunitwizard.kernel as kernel
from pyunitwizard._private.exceptions import ArgumentError


def test_conversion_factor_length():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.conversion_factor('nm', 'angstroms') == pytest.approx(10.0)
    assert puw.conversion_factor('angstroms', 'nm') == pytest.approx(0.1)


def test_conversion_factor_area_and_volume():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.conversion_factor('nm**2', 'angstroms**2') == pytest.approx(100.0)
    assert puw.conversion_factor('nm**3', 'angstroms**3') == pytest.approx(1000.0)


def test_conversion_factor_matches_convert():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    factor = puw.conversion_factor('nm', 'angstroms')
    value = 0.14
    expected = puw.get_value(puw.quantity(value, 'nm'), to_unit='angstroms')
    assert value * factor == pytest.approx(expected)


def test_conversion_factor_is_cached():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert not any(
        k[0] == 'nm' and k[1] == 'angstroms'
        for k in kernel.conversion_factor_cache
    )
    first = puw.conversion_factor('nm', 'angstroms')
    assert any(
        k[0] == 'nm' and k[1] == 'angstroms'
        for k in kernel.conversion_factor_cache
    )
    second = puw.conversion_factor('nm', 'angstroms')
    assert first == second


def test_conversion_factor_affine_units_raise():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    with pytest.raises(ArgumentError):
        puw.conversion_factor('degC', 'kelvin')
