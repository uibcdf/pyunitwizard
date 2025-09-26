import pytest

import pyunitwizard as puw

astropy_units = pytest.importorskip("astropy.units")
from astropy import units as u


@pytest.fixture
def astropy_setup():
    loaded_before = list(puw.configure.get_libraries_loaded())
    default_form = puw.configure.get_default_form()
    default_parser = puw.configure.get_default_parser()

    puw.configure.reset()
    puw.configure.load_library(["pint", "astropy.units"])

    yield

    puw.configure.reset()
    if loaded_before:
        puw.configure.load_library(loaded_before)
        if default_form is not None:
            puw.configure.set_default_form(default_form)
        if default_parser is not None:
            puw.configure.set_default_parser(default_parser)


def test_get_form_astropy_quantity(astropy_setup):
    quantity = 5.0 * u.m
    assert puw.get_form(quantity) == "astropy.units"


def test_is_quantity_and_unit(astropy_setup):
    quantity = 3.0 * u.s
    assert puw.is_quantity(quantity)
    assert puw.is_unit(quantity.unit)


def test_convert_within_astropy(astropy_setup):
    quantity = 2.0 * u.m
    converted = puw.convert(quantity, to_unit="cm")
    assert puw.get_form(converted) == "astropy.units"
    assert puw.get_value(converted) == pytest.approx(200.0)


def test_convert_to_pint(astropy_setup):
    quantity = 7.0 * u.kg
    pint_quantity = puw.convert(quantity, to_form="pint")
    pytest.importorskip("pint")
    from pint import Quantity as PintQuantity

    assert isinstance(pint_quantity, PintQuantity)
    assert pint_quantity.magnitude == pytest.approx(7.0)
    assert str(pint_quantity.units) == "kilogram"


def test_dimensionality(astropy_setup):
    quantity = 3.0 * u.m / u.s
    dims = puw.get_dimensionality(quantity)
    assert dims["[L]"] == pytest.approx(1.0)
    assert dims["[T]"] == pytest.approx(-1.0)


def test_compatibility(astropy_setup):
    assert puw.are_compatible(u.m, u.cm)


def test_string_parser(astropy_setup):
    quantity = puw.convert("10 m", to_form="astropy.units", parser="astropy.units")
    assert puw.is_quantity(quantity)
    assert puw.get_value(quantity) == pytest.approx(10.0)
    assert puw.get_form(quantity) == "astropy.units"


def test_quantity_constructor(astropy_setup):
    quantity = puw.quantity(1.5, unit=u.km, form="astropy.units")
    assert puw.is_quantity(quantity)
    assert puw.get_unit(quantity).is_equivalent(u.m)
    assert puw.get_value(puw.convert(quantity, to_unit="m")) == pytest.approx(1500.0)


def test_to_string_conversion(astropy_setup):
    quantity = 1.2 * u.m
    string_quantity = puw.to_string(quantity, to_unit="cm")
    assert "120" in string_quantity
    assert "cm" in string_quantity
