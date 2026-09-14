import openmm.unit as openmm_unit
import pytest
import unyt

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError


def test_are_equal_parsing_error():

    with pytest.raises(LibraryWithoutParserError):
        puw.configure.reset()
        puw.configure.load_library(["openmm.unit"])
        puw.are_equal("1 meter", "1 meter")


def test_are_equal_string_quantity():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])

    equal = puw.are_equal("1 meter", "1 kilometer")
    assert not equal

    equal = puw.are_equal("1 meter", "1 cm")
    assert not equal

    equal = puw.are_equal("1 meter", "100 cm")
    assert equal


def test_are_equal_pint_quantity():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    quantity_1 = puw.quantity(0.4, "cm", form="pint")
    quantity_2 = puw.quantity(0.4, "cm", form="pint")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, "mm", form="pint")
    quantity_2 = puw.quantity(0.4, "cm", form="pint")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, "mm", form="pint")
    quantity_2 = puw.quantity(0.41, "cm", form="pint")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal

    quantity_1 = puw.quantity(4, "m", form="pint")
    quantity_2 = puw.quantity(4, "cm", form="pint")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal


def test_are_equal_openmm_quantity():
    puw.configure.reset()
    puw.configure.load_library(["openmm.unit"])

    quantity_1 = puw.quantity(0.4, openmm_unit.centimeter, form="openmm.unit")
    quantity_2 = puw.quantity(0.4, openmm_unit.centimeter, form="openmm.unit")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, openmm_unit.millimeter, form="openmm.unit")
    quantity_2 = puw.quantity(0.4, openmm_unit.centimeter, form="openmm.unit")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, openmm_unit.millimeter, form="openmm.unit")
    quantity_2 = puw.quantity(0.41, openmm_unit.centimeter, form="openmm.unit")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal

    quantity_1 = puw.quantity(1, openmm_unit.meter, form="openmm.unit")
    quantity_2 = puw.quantity(1, openmm_unit.centimeter, form="openmm.unit")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal


def test_are_equal_unyt_quantity():
    puw.configure.reset()
    puw.configure.load_library(["unyt"])

    quantity_1 = puw.quantity(0.4, unyt.cm, form="unyt")
    quantity_2 = puw.quantity(0.4, unyt.cm, form="unyt")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, unyt.mm, form="unyt")
    quantity_2 = puw.quantity(0.4, unyt.cm, form="unyt")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert equal

    quantity_1 = puw.quantity(4, unyt.mm, form="unyt")
    quantity_2 = puw.quantity(0.41, unyt.cm, form="unyt")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal

    quantity_1 = puw.quantity(4, unyt.m, form="unyt")
    quantity_2 = puw.quantity(4, unyt.cm, form="unyt")
    equal = puw.are_equal(quantity_1, quantity_2)
    assert not equal


def test_are_equal_string():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    equal = puw.are_equal("0.0 degrees", "0.0 radians")
    assert equal

    equal = puw.are_equal("4 mm", "0.4 cm")
    assert equal

    equal = puw.are_equal("4 mm", "0.41 cm")
    assert not equal

    equal = puw.are_equal("4 m", "4 cm")
    assert not equal
