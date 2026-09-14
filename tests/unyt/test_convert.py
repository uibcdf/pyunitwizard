import numpy as np
import openmm.unit as openmm_unit
import unyt

import pyunitwizard as puw


def test_convert_from_unyt_to_unyt():
    puw.configure.reset()
    puw.configure.load_library(["unyt", "pint"])
    puw.configure.set_default_parser("pint")

    quantity = puw.convert(1 * unyt.m, to_unit="cm")
    assert quantity == 100.0 * unyt.cm

    quantity = puw.convert(1 * unyt.m, to_type="unit")
    assert isinstance(quantity, unyt.Unit)
    assert str(quantity) == "m"

    quantity = puw.convert(1 * unyt.m, to_unit=unyt.cm, to_type="unit")
    assert isinstance(quantity, unyt.Unit)
    assert str(quantity) == "cm"

    quantity = puw.convert(1 * unyt.m, to_type="value")
    assert quantity == 1

    quantity = puw.convert(1 * unyt.m, to_unit=unyt.cm, to_type="value")
    assert quantity == 100.0


def test_convert_from_unyt_to_pint():
    puw.configure.reset()
    puw.configure.load_library(["unyt", "pint"])

    quantity = puw.convert(1 * unyt.m, to_form="pint")
    assert puw.get_form(quantity) == "pint"
    assert puw.get_value(quantity) == 1
    assert puw.get_unit(quantity) == "meter"

    quantity = puw.convert([1.0, 2.0] * unyt.m, to_form="pint")
    assert puw.get_form(quantity) == "pint"
    assert np.all(puw.get_value(quantity) == [1.0, 2.0])
    assert puw.get_unit(quantity) == "meter"


def test_convert_from_unyt_to_openmm():
    puw.configure.reset()
    puw.configure.load_library(["openmm.unit", "unyt"])

    quantity = puw.convert(1 * unyt.m, to_form="openmm.unit")
    assert puw.get_form(quantity) == "openmm.unit"
    assert puw.get_value(quantity) == 1
    assert puw.get_unit(quantity) == openmm_unit.meter

    quantity = puw.convert([1.0, 2.0] * unyt.m, to_form="openmm.unit")
    assert puw.get_form(quantity) == "openmm.unit"
    assert np.all(puw.get_value(quantity) == [1.0, 2.0])
    assert puw.get_unit(quantity) == openmm_unit.meter


def test_convert_from_unyt_to_string():
    puw.configure.reset()
    puw.configure.load_library(["unyt"])

    quantity = puw.convert(1 * unyt.m, to_unit=unyt.cm, to_form="string")
    assert quantity == "100.0 cm"

    unit = puw.convert(1 * unyt.m, to_unit=unyt.cm, to_form="string", to_type="unit")
    assert unit == "cm"
