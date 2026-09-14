import numpy as np
import openmm.unit as openmm_unit
import unyt

import pyunitwizard as puw

## Test converting from string to pint ##


def test_convert_from_string_to_pint():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    ureg = puw.forms.api_pint.ureg

    quantity = puw.convert("1 meter")
    assert quantity == ureg.Quantity(1, "meter")

    quantity = puw.convert("1 meter", to_unit="cm")
    assert quantity == ureg.Quantity(100.0, "centimeter")

    quantity = puw.convert("1 meter", to_type="unit")
    assert quantity == ureg.Unit("meter")

    quantity = puw.convert("1 meter", to_unit="cm", to_type="unit")
    assert quantity == ureg.Unit("centimeter")


def test_convert_from_string_to_string():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    quantity = puw.convert("1 meter", to_unit="cm", to_form="string")
    assert quantity == "100.0 centimeter"

    quantity = puw.convert("1 meter", to_unit="cm", to_form="string", to_type="unit")
    assert quantity == "centimeter"

    quantity = puw.convert("1 meter", to_type="value")
    assert quantity == 1

    quantity = puw.convert("1 meter", to_unit="cm", to_type="value")
    assert quantity == 100.0

    quantity = puw.convert("100 angstroms**3", to_form="string", to_type="unit")
    assert quantity == "angstrom ** 3"


## Test converting from pint to pint ##


def test_convert_from_pint_to_pint():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    ureg = puw.forms.api_pint.ureg
    quantity = ureg.Quantity(2.5, "nanometers/picoseconds")
    quantity = puw.convert(quantity, to_unit="angstroms/picoseconds")
    assert quantity == ureg.Quantity(25.0, "angstroms/picoseconds")


## Test converting from pint to opemmm.unit ##


def test_convert_from_pint_to_openmm_unit():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    ureg = puw.forms.api_pint.ureg

    quantity = ureg.Quantity(2.5, "nanometers/picoseconds")
    quantity = puw.convert(quantity, to_form="openmm.unit")
    assert quantity == 2.5 * openmm_unit.nanometer / openmm_unit.picosecond

    unit_openmm = puw.unit("nm", form="openmm.unit")
    unit_pint = puw.unit("nm", form="pint")
    assert unit_openmm == puw.convert(unit_pint, to_form="openmm.unit")


def test_convert_from_pint_to_openmm_array():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    ureg = puw.forms.api_pint.ureg

    quantity = ureg.Quantity([2, 3, 7], "meter")
    quantity = puw.convert(quantity, to_form="openmm.unit")
    quantity_true = np.array([2, 3, 7]) * openmm_unit.meter
    assert np.all(quantity == quantity_true)

    quantity = ureg.Quantity([[0, 0], [0, 0]], "nanometers/picoseconds")
    quantity = puw.convert(quantity, to_form="openmm.unit")
    q_true = [[0, 0], [0, 0]] * openmm_unit.nanometer / openmm_unit.picosecond
    assert np.all(quantity == q_true)


## Test converting from pint to unyt ##
def test_convert_from_pint_to_unyt():
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])
    ureg = puw.forms.api_pint.ureg

    quantity = ureg.Quantity(2.5, "nanometers/picoseconds")
    quantity = puw.convert(quantity, to_form="unyt")
    assert quantity == 2.5 * unyt.nm / unyt.ps


def test_convert_from_pint_to_unyt_array():
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])
    ureg = puw.forms.api_pint.ureg

    quantity = ureg.Quantity([2, 3, 7], "meter")
    quantity = puw.convert(quantity, to_form="unyt")
    quantity_true = np.array([2, 3, 7]) * unyt.m
    assert np.all(quantity == quantity_true)

    quantity = ureg.Quantity([[0, 0], [0, 0]], "nanometers/picoseconds")
    quantity = puw.convert(quantity, to_form="unyt")
    q_true = [[0, 0], [0, 0]] * unyt.nm / unyt.ps
    assert np.all(quantity == q_true)
