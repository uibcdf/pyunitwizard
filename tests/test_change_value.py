import unyt

import pyunitwizard as puw


def test_quantity_openmm_unit():

    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])

    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    quantity = puw.quantity("10 kilojoule/mole", form="openmm.unit")
    quantity = puw.change_value(quantity, 20)
    quantity_true = 20 * openmm_unit.kilojoule / openmm_unit.mole
    assert puw.are_close(quantity, quantity_true)


def test_quantity_pint():

    puw.configure.reset()
    puw.configure.load_library(["pint"])

    ureg = puw.forms.api_pint.ureg
    quantity = puw.quantity(10, "nanometers/picoseconds")
    quantity = puw.change_value(quantity, 20)
    quantity_true = ureg.Quantity(20, "nanometers/picoseconds")
    assert puw.are_close(quantity, quantity_true)


def test_quantity_unyt():

    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])

    quantity = puw.quantity(10, unyt.J / unyt.s, form="unyt")
    quantity = puw.change_value(quantity, 20)
    quantity_true = 20 * unyt.J / unyt.s
    assert puw.are_close(quantity, quantity_true)
