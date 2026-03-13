# This file contains test for get_unit, get_value, and get_dimensionality
import pyunitwizard as puw
import pytest
import unyt
import numpy as np

astropy_units = pytest.importorskip("astropy.units")
from astropy import units as u

@pytest.fixture
def pint_unit_registry():
    """ Returns a pint unit registry"""
    return puw.forms.api_pint.ureg

@pytest.fixture
def pint_quantity(pint_unit_registry):
    """ Returns a pint.Quantity"""
    return pint_unit_registry.Quantity(2.5, 'nanometers/picoseconds')

@pytest.fixture
def openmm_quantity():
    """ Returns an openmm quantity"""
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    return 2.5 * openmm_unit.nanometer/openmm_unit.picoseconds

@pytest.fixture
def unyt_quantity():
    """Returns a unyt quantity"""
    return 2.5 * unyt.nm/unyt.ps

#### Tests for get value ####

def test_get_value_pint(pint_quantity):
    assert puw.get_value(pint_quantity) == 2.5

def test_get_value_openmm(openmm_quantity):
    assert puw.get_value(openmm_quantity) == 2.5

def test_get_value_unyt(unyt_quantity):
    assert puw.get_value(unyt_quantity) == 2.5

def test_get_value_astropy_returns_numeric_scalar():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'astropy.units'])

    quantity = 2.0 * u.m
    converted = puw.convert(quantity, to_unit='cm')
    value = puw.get_value(converted)

    assert value == pytest.approx(200.0)
    assert not puw.is_quantity(value)

def test_get_value_standardized_ignores_to_unit():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, 'meter')
    value = puw.get_value(quantity, to_unit='meter', standardized=True)

    assert value == pytest.approx(1e9)


def test_get_value_supports_value_type_and_dtype():
    quantity = puw.quantity([[1, 2, 3]], "nanometer")

    value = puw.get_value(quantity, value_type="numpy.ndarray", dtype=np.float32)

    assert isinstance(value, np.ndarray)
    assert value.dtype == np.float32
    assert value.shape == (1, 3)


def test_get_value_supports_list_output():
    quantity = puw.quantity(np.array([1.0, 2.0, 3.0]), "nanometer")

    value = puw.get_value(quantity, value_type="list")

    assert value == [1.0, 2.0, 3.0]

#### Tests for get unit ####

def test_get_unit_pint(pint_unit_registry, pint_quantity):
    unit_true = pint_unit_registry.Unit('nanometers/picoseconds')
    assert puw.get_unit(pint_quantity) == unit_true

def test_get_unit_openmm(openmm_quantity):
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    unit = puw.get_unit(openmm_quantity)
    assert isinstance(unit, openmm_unit.Unit)
    assert str(unit) == "nanometer/picosecond"

def test_get_unit_unyt(unyt_quantity):
    unit = puw.get_unit(unyt_quantity)
    assert isinstance(unit, unyt.Unit)
    assert str(unit) == "nm/ps"

def test_get_unit_standardized_path():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, 'meter')
    unit = puw.get_unit(quantity, to_form='string', standardized=True)

    assert unit == 'nanometer'

#### Tests for get value and unit ####

def test_get_value_and_unit_pint(pint_unit_registry, pint_quantity):
    unit_true = pint_unit_registry.Unit('nanometers/picoseconds')
    value_true = 2.5
    value, unit = puw.get_value_and_unit(pint_quantity)
    assert value == value_true
    assert unit == unit_true

def test_get_value_and_unit_openmm(openmm_quantity):
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    value, unit = puw.get_value_and_unit(openmm_quantity)
    value_true = 2.5
    assert isinstance(unit, openmm_unit.Unit)
    assert str(unit) == "nanometer/picosecond"
    assert value == value_true

def test_get_value_and_unit_unyt(unyt_quantity):
    value, unit = puw.get_value_and_unit(unyt_quantity)
    value_true = 2.5
    assert isinstance(unit, unyt.Unit)
    assert str(unit) == "nm/ps"
    assert value == value_true

def test_get_value_and_unit_standardized_ignores_to_unit():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, 'meter')
    value, unit = puw.get_value_and_unit(
        quantity,
        to_unit='meter',
        to_form='string',
        standardized=True,
    )

    assert value == pytest.approx(1e9)
    assert unit == 'nanometer'


def test_get_value_and_unit_supports_value_type_and_dtype():
    quantity = puw.quantity([[1, 2, 3]], "nanometer")

    value, unit = puw.get_value_and_unit(
        quantity,
        value_type="numpy.ndarray",
        dtype=np.float32,
        to_form="string",
    )

    assert isinstance(value, np.ndarray)
    assert value.dtype == np.float32
    assert unit == "nanometer"

#### Tests for get dimensionality ####

def test_get_dimensionality_pint(pint_quantity):
    assert puw.get_dimensionality(pint_quantity) == {'[L]': 1, '[M]': 0, 
                                                    '[T]': -1, '[K]': 0, 
                                                    '[mol]': 0, '[A]': 0, 
                                                    '[Cd]': 0}

def test_get_dimensionality_openmm(openmm_quantity):
    assert puw.get_dimensionality(openmm_quantity) == {'[L]': 1, '[M]': 0, 
                                                    '[T]': -1, '[K]': 0, 
                                                    '[mol]': 0, '[A]': 0, 
                                                    '[Cd]': 0}

def test_get_dimensionality_unyt(unyt_quantity):
    assert puw.get_dimensionality(unyt_quantity) == {'[L]': 1, '[M]': 0, 
                                                    '[T]': -1, '[K]': 0, 
                                                    '[mol]': 0, '[A]': 0, 
                                                    '[Cd]': 0}
