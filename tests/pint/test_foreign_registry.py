"""Pint quantities from other registries must enter the shared kernel safely."""

import pint
import pytest

import pyunitwizard as puw
from pyunitwizard.forms import api_pint


def test_foreign_pint_quantity_is_recognized_and_rebuilt_in_kernel_registry():
    foreign = pint.UnitRegistry()
    quantity = foreign.Quantity(3.0, "nanometer")

    assert puw.get_form(quantity) == "pint"
    assert puw.is_quantity(quantity)
    assert puw.is_unit(quantity.units)

    converted = puw.convert(quantity, to_form="pint")
    assert converted._REGISTRY is api_pint.ureg
    assert converted.magnitude == pytest.approx(3.0)
    assert converted + api_pint.ureg.Quantity(1.0, "nanometer") == api_pint.ureg.Quantity(4.0, "nanometer")
    assert puw.convert(quantity)._REGISTRY is api_pint.ureg
    assert puw.convert(quantity, to_unit="angstrom").magnitude == pytest.approx(30.0)


def test_foreign_pint_quantity_with_different_definition_is_rejected():
    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("nanometer = 2e-9 * meter = nm")
    quantity = foreign.Quantity(3.0, "nanometer")

    with pytest.raises(ValueError, match="different definition"):
        puw.convert(quantity, to_form="pint")


def test_foreign_affine_pint_unit_retains_its_offset():
    foreign = pint.UnitRegistry()
    quantity = foreign.Quantity(25.0, "degree_Celsius")

    converted = puw.convert(quantity, to_unit="kelvin", to_form="pint")
    assert converted._REGISTRY is api_pint.ureg
    assert converted.magnitude == pytest.approx(298.15)
