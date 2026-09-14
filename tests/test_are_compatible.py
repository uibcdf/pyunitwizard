import openmm.unit as openmm_unit
import unyt

import pyunitwizard as puw


def test_are_compatible_pint():

    puw.configure.reset()
    puw.configure.load_library(["pint"])

    q1 = puw.quantity(2.5, "nanometers/picoseconds", form="pint")
    q2 = puw.convert(q1, to_unit="angstroms/picoseconds", to_form="pint")
    assert puw.are_compatible(q1, q2)

    q1 = puw.quantity(2.5, "joules/picoseconds", form="pint")
    q2 = puw.quantity(2.8, "angstroms/picoseconds", form="pint")
    assert not puw.are_compatible(q1, q2)


def test_are_compatible_openmm():

    puw.configure.reset()
    puw.configure.load_library(["openmm.unit"])

    q1 = puw.quantity(2.5, openmm_unit.nanometer / openmm_unit.picosecond, form="openmm.unit")
    q2 = puw.quantity(3.0, openmm_unit.angstrom / openmm_unit.second, form="openmm.unit")
    assert puw.are_compatible(q1, q2)

    q1 = puw.quantity(2.5, openmm_unit.joule / openmm_unit.second, form="openmm.unit")
    q2 = puw.quantity(3.0, openmm_unit.angstrom / openmm_unit.second, form="openmm.unit")
    assert not puw.are_compatible(q1, q2)


def test_are_compatible_unyt():

    puw.configure.reset()
    puw.configure.load_library(["unyt"])

    q1 = puw.quantity(2.5, unyt.nm / unyt.ps, form="unyt")
    q2 = puw.quantity(3.0, unyt.m / unyt.second, form="unyt")
    assert puw.are_compatible(q1, q2)

    q1 = puw.quantity(2.5, unyt.J / unyt.second, form="unyt")
    q2 = puw.quantity(3.0, unyt.m / unyt.second, form="unyt")
    assert not puw.are_compatible(q1, q2)


def test_are_compatible_string():

    puw.configure.reset()
    puw.configure.load_library(["pint"])

    assert puw.are_compatible("0.0 degrees", "0.0 radians")

    assert not puw.are_compatible("2.5 J/s", "3.0 m/s")
